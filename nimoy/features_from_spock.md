# Features from Spock


* Tests are gathered in Specification classes, each specification specifies a module, class or flow.
  - Specifications are encapsulated
  - Specifications support fixtures, possibly inheriting from unittest and Django's fixtures
  - Specifications can have helper methods which will not be run as tests.
  - Tests are gathered in "feature" methods
* Fixtures
  - `setup` - before every feature
  - `cleanup` - after every feature
  - `spec_setup` - before first feature
  - `spec_cleanup` - after the last feature
  - Support unittest 's `fixtures` class field for loading fixture files
* Feature methods
  - Feature methods are any methods decorated with `@feature(name)` decorator
    _Python cannot support Groovy's awesome method-name-as-a-string, so we will use the feature decorator instead_
  - A feature is broken up to blocks, which are: `setup`, `when`, `then`, `expect` and `cleanup`.
  - Feature blocks are indicated by `with <block>` statements, E.G:
    ```python
    @feature("Use of blocks")
    def feature_blocks(self):
      with setup():
        # We do some setup here
      with when():
        # Run some code
      with then():
        # Check some expectations, e.g. values where set, exceptions raised, mock methods were called etc.
      with cleanup():
        # Do some cleanup
    ```
    The `expect` block is basically `when` and `then` blocks combined.
  - `when` and `then` blocks are tightly coupled. A `when` block can have
  - Features can have a `@where` decorator. `@where` injects variables into the feature method scope, and runs
    it repeatedly with all possible values, E.G:
    ```python
    @feature("Check border conditions")
    @where(variable='in', is=['', 'legal value', 'illegal value', 'bah' * 2000])
    def feature_border_conditions(self, in):
      # Feature will be executed once for every value of 'in'
    ```
    The `variable` can be a tuple of values, and each value of `is` will be unpacked into these variable names.
    Another possible syntax is stating 'is' as a dictionary of lists, with variable names as keys, iterating all
    combinations.
    Third possible syntax is a list of dictionaries, keys are variable names.
    