# User Guide

## Installation

    pip install nimoy-framework
    
## Quickstart

Let's create your first spec!

### Project Structure

Within your project directory create a `specs` directory:

```
.
+-- mymodule/
    +-- __init__.py
    +-- my_module.py
+-- specs/              <-- Added a new folder for the specifications
    +-- __init__.py
+-- README.md
+-- index.html 
```

### Nimoy Modules

Ideally every one of your Python modules may be represented by a Nimoy module, so you can mimic your application's directory structure within the `specs` folder.

Within the specs folder create a new module named `my_module_spec.py`.

**Note**: Nimoy will only pick up on modules ending with `_spec.py`.

```
.
+-- mymodule/
    +-- __init__.py
    +-- my_module.py
+-- specs/
    +-- __init__.py
    +-- my_module_spec.py <-- Added a new folder for the specifications
+-- README.md
+-- index.html 
```

### Your First Specification

To be considered as a specification, your class must end with the name `Spec` and must extend the `Specification` class.

Any public method within the specification class will be treated as a feature method.
```python
# my_module_spec.py

from nimoy.specification import Specification

# The class name ends with Spec and extends Specification
class MyFirstSpec(Specification):

    # The feature method is public
    def my_feature_method(self):
        with given:
            a = 'The quick brown fox'
        with expect:
            a == 'The quick frown box'
            
    # This is not a feature method
    def _helper_method(self):
       pass
```

### Running Your Specification

Simply execute `nimoy` within your project directory. Nimoy will auto-discover all your specs!

```bash
$ nimoy

my_feature_method (builtins.MyFirstSpec) ... FAIL

======================================================================
FAIL: my_feature_method (builtins.MySpec)
----------------------------------------------------------------------
AssertionError:
Expected: 'The quick frown box'
     but: was 'The quick brown fox'
Hint:
- The quick brown fox
?           ^     ^

+ The quick frown box
?           ^     ^


----------------------------------------------------------------------
Ran 1 test in 0.002s

FAILED (failures=1)
```