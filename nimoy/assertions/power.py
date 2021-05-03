from nimoy.compare.types import Types


class Expression:
    def __init__(self, name: str, value, column: int, constant: bool = False, next_node=None):
        self.name = name
        self.value = value
        self.column = column
        self.constant = constant
        self.next_node = next_node


class Op:
    def __init__(self, value: str, op: Types):
        self.value = value
        self.op = op


class Assertion:
    def __init__(self, left: Expression, right: Expression, op: Op):
        self.left = left
        self.right = right
        self.op = op


class PowerAssertions:

    def __init__(self):
        # This var keeps track of value columns - columns where an expression begins and that expression has a value
        # that needs to be rendered. This is so we know where to position all different the pipes (|) that lead from a
        # value to its expression in the final render
        self.columns = {}

        # This var changes in place and represents a single value row in the final render. It keeps track of the values
        # that need to be listed in the row of the current iterations. A row breaks whenever a value of an expression
        # is longer than the expression itself. When a value is longer, it can break the column of the next expression
        self.current_value_row = []

        # Collection of all rendered value rows
        self.value_rows = []

        # We use this var to keep track of our position in the expression during the iteration
        self.current_index = 0

    def _append_and_reset_current_value_row(self):
        joined_value_row = ''.join(self.current_value_row)

        # Extra spaces may have been prematurely added for padding. Remove them only on the right because whitespace
        # after the last listed value on that row is unnecessary
        trimmed_value_row = joined_value_row.rstrip()
        self.value_rows.append(trimmed_value_row)
        self.current_value_row = []

    def _append_assertion_node(self, assertion, side_expression):
        # Starting with the left most node
        current_node = assertion
        while current_node is not None:

            # First, add the name of the current node to the left side of the expression for the final render
            side_expression.append(current_node.name)

            # If we are starting with an empty value row, we need to start filling it
            if len(self.current_value_row) == 0:

                # Before we add the value of the current row, we need to check if there are any previous values that
                # have been listed. Go through columns from 0 to the column of the current value, and fill in a pipe if
                # there was a value at that column, or a space if there was no value at than column
                for column in range(current_node.column):
                    if column in self.columns and self.columns[column]:
                        self.current_value_row.append('|')
                    else:
                        self.current_value_row.append(' ')

            # Finally, if the current node isn't a constant, append the value of the current node to the current value
            # row and list the column for later iterations. Constants should be added to the value rows as its redundant
            if not current_node.constant:
                self.current_value_row = self.current_value_row + list(str(current_node.value))
                self.columns[current_node.column] = True

            # If the value of the current node is longer than the expression itself, we need to start a new value row
            # because this value may leak into the next value column
            if len(str(current_node.value)) > len(current_node.name):

                # Add the current value row to the list of finalized value rows and reset the current value row
                self._append_and_reset_current_value_row()

            # The value of the current node is equal or shorter than the name of the node
            else:
                # Pad the current value row with spaces for the remainder of the length of the current expression,
                # ready for the next expression
                length_of_range_to_pad = len(current_node.name) - len(str(current_node.value))
                if length_of_range_to_pad == 0 and current_node.constant:
                    length_of_range_to_pad = len(current_node.name)
                for column in range(length_of_range_to_pad):
                    self.current_value_row.append(' ')

            # Bump the current index with the length of the current node name ready for the next iteration and move to
            # the next node
            self.current_index = (current_node.column + len(current_node.name)) - 1
            current_node = current_node.next_node

    def assert_and_render(self, assertion: Assertion):

        # This var keeps all the expressions to the left of the comparator. We keep track of this so that we can later
        # render the complete expression
        left_expression = []

        self._append_assertion_node(assertion.left, left_expression)

        # We've completed the iteration over the left expression, now manually add the location of the comparator to the
        # columns because we track the value of the comparator as well
        self.current_index = self.current_index + 2
        self.columns[self.current_index] = True

        # Append the value of the comparator (True / False) to the current value row
        self.current_value_row = self.current_value_row + list(str(f' {assertion.op.value}'))

        # Add the current value row to the list of finalized value rows and reset the current value row
        self._append_and_reset_current_value_row()

        # Bump the current index in preparation for the iteration of the right expression
        self.current_index = self.current_index + 2

        right_expression = []
        self._append_assertion_node(assertion.right, right_expression)

        # Add the current value row to the list of finalized value rows and reset the current value row
        self._append_and_reset_current_value_row()

        # If the last expression on the right was a literal, a row of all pads and pipes will have already been added
        # because the first thing we do when we handle a new expression node is to pad and pipe for all prior values.
        # In the case of a literal the row will be padded and piped but no value will be added.
        # In all other cases we need to create this first row with all pads and pipes
        last_added_row = self.value_rows[-1]
        if any(letter.isalnum() for letter in last_added_row):
            for column in range(max(self.columns.keys()) + 1):
                if column in self.columns and self.columns[column]:
                    self.current_value_row.append('|')
                else:
                    self.current_value_row.append(' ')

            # Add the current value row to the list of finalized value rows and reset the current value row
            self._append_and_reset_current_value_row()

        self.value_rows.reverse()

        joined_values = "\n".join(self.value_rows) + '\n'
        value = f"Assertion failed:\n{'.'.join(left_expression)} == {'.'.join(right_expression)}\n{joined_values}"
        return value
