from typing import Dict


# Renders this:
# my_var.my_field == my_var_2
#
# To this:
# Assertion failed:
# my_var.my_field == my_var_2
# |      |        |  |
# |      |        |  {'bob': 'mcbob'}
# |      2        false
# {'moo': 'bob'}
#
# The input of the assertion methods is the assertion expression broken in a tree structure that can be produced using
# nimoy.ast_tools.expression_transformer.PowerAssertionTransformer
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

        # This var keeps the rendered expression. We keep track of this so that we can later display it in the message
        self.rendered_expression = []

    # Document the value in the value row
    def _append_value_to_current_value_row(self, node_name: str, node_value: str, node_column: int, constant: bool):
        # If we are starting with an empty value row, we might need to fill it with pads and pipes of previous values
        if len(self.current_value_row) == 0:

            # Before we add the value to the current row, we need to check if there are any previous values that have
            # been listed. Go through columns from 0 to the given column, and fill in a pipe if there was a value at
            # that column, or a space if there was no value at that column
            for column in range(node_column):
                if column in self.columns and self.columns[column]:
                    self.current_value_row.append('|')
                else:
                    self.current_value_row.append(' ')

        # Finally, if the value isn't a constant, append the value to the current row and document the column for later
        # iterations. Constants should be added to the value rows as its redundant
        if not constant:
            self.current_value_row = self.current_value_row + list(str(node_value))

            # Document that there's a value in this column for later iterations
            self.columns[node_column] = True

        # If the value of the node is longer than the name of the node, we need to start a new value row because this
        # value may leak into the starting column of the next node
        if len(str(node_value)) > len(node_name):

            # Add the current value row to the list of finalized value rows and reset the current value row
            self._append_and_reset_current_value_row()

        # The value of the current node is equal to or shorter than the name of the node
        else:
            # Pad the current value row with spaces for the remainder of the length of the current node, ready for the
            # next node
            length_of_range_to_pad = len(node_name) - len(str(node_value))
            if length_of_range_to_pad == 0 and constant:
                length_of_range_to_pad = len(node_name)

            for column in range(length_of_range_to_pad):
                self.current_value_row.append(' ')

            # Add another pad to account for the separator between this node and the next
            self.current_value_row.append(' ')

    # Adds the current value row to the list of value rows to be rendered and reset it ready for the next iteration
    def _append_and_reset_current_value_row(self):

        # If the current value row is empty, then we don't need to add anything. This may happen when the last value row
        # exceeded the length of the whole expression. In this case the value row was already appended to the render
        # list and reset
        if not self.current_value_row:
            return

        joined_value_row = ''.join(self.current_value_row)

        # Extra spaces may have been prematurely added for padding. Remove them only on the right because whitespace
        # after the last listed value on that row is unnecessary
        trimmed_value_row = joined_value_row.rstrip()
        self.value_rows.append(trimmed_value_row)
        self.current_value_row = []

    # Iterates over the expression hierarchy to build the complete asserted expression and the value breakdown
    def _append_expression(self, expression: Dict):

        # Starting with the left most node
        current_node = expression
        while current_node is not None:

            # If the current node is a comparison operation
            if current_node['type'] == 'op':

                # Append the actual operation (== for example) to the rendered assertion expression
                self.rendered_expression.append(current_node['op'])

                # The operation name has been added to the expression, now we add the separator between this node and
                # the next node. This is always a space
                self.rendered_expression.append(' ')

                # Append the outcome of the assertion (true/false) to the current value row
                self._append_value_to_current_value_row(current_node['type'], current_node['value'],
                                                        current_node['column'], False)

            # Current node is an expression
            else:
                # Append the name of the node (my_var for example) to the rendered assertion expression
                self.rendered_expression.append(current_node['name'])

                # The current node name has been added to the expression, now we add the separator between this node and
                # the next node. This is either a period or a space
                if current_node.get('next'):
                    if current_node['next']['type'] == 'exp':
                        self.rendered_expression.append('.')
                    if current_node['next']['type'] == 'op':
                        self.rendered_expression.append(' ')

                # Append the value of the node ('my_value' for example) to the current value row
                self._append_value_to_current_value_row(current_node['name'], current_node['value'],
                                                        current_node['column'],
                                                        current_node.get('constant', False))

            current_node = current_node.get('next')

    # Renders a Nimoy power assertion expression a string
    def render(self, expression: Dict):

        # Append all expression nodes to the global data structures
        self._append_expression(expression)

        # Append any content that's been added to the current value row
        self._append_and_reset_current_value_row()

        # If the last expression on the right was a literal, a row of all pads and pipes will have already been added
        # because the first thing we do when we handle a new expression node is to pad and pipe for all values that have
        # appeared beforehand.
        # In the case of a literal the row will be padded and piped but when the literal is reached, its value will not
        # be added.
        # In all other cases we need to create this first row with all pads and pipes
        last_added_row = self.value_rows[-1]

        # Check if the last row contains *any* alphanumeric characters. If it does we need to create the all pipe/pad
        # row
        if any(letter.isalnum() for letter in last_added_row):

            # Iterate from zero to the right-most value column
            for column in range(max(self.columns.keys()) + 1):

                # If theres a value in this column, write a pipe
                if column in self.columns and self.columns[column]:
                    self.current_value_row.append('|')
                else:
                    self.current_value_row.append(' ')

            # Add the current value row to the list of finalized value rows and reset the current value row
            self._append_and_reset_current_value_row()

        self.value_rows.reverse()

        joined_value_rows = "\n".join(self.value_rows) + '\n'
        value = f"Assertion failed:\n{''.join(self.rendered_expression)}\n{joined_value_rows}"
        return value

    # Raises an AssertionError if the expression failed
    def assert_and_raise(self, expression: Dict):
        # Look for the op and inspect its value
        current_node = expression
        while current_node is not None:
            if current_node['type'] != 'op':
                current_node = current_node.get('next')
                continue

            # If the assertion op succeeded, return. There's no need to render anything
            if current_node['value']:
                return

            # If the assertion failed
            break

        raise AssertionError(self.render(expression))
