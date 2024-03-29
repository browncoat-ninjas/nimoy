# Examples

## Pretty Failure Messages

### Power Assertions (Beta):

Power assertions is in beta! This feature can be turned on using the `--power-assertions` switch.

Taking inspiration from [Groovy](http://docs.groovy-lang.org/next/html/documentation/core-testing-guide.html#_power_assertions), power assertions take the failed assertion statement and break it down so that you can better understand the problem.

```python
from nimoy.specification import Specification

class MySpec(Specification):
    
    def use_power_assertions(self):
        with setup:
            class SomeClass:
                def __init__(self):
                    self.val = {'d': 'e'}
                    
                def __str__(self):
                    return str(self.val)

            sc = SomeClass()
        with expect:
            sc.val['d'] == 'f'
```

Running this spec using `nimoy --power-assertions true` produces:

```
======================================================================
FAIL: use_power_assertions (builtins.MySpec)
----------------------------------------------------------------------
Traceback (most recent call last):
  [redacted]
AssertionError: Assertion failed:
sc.val['d'] == f
|  |        |
|  e        False
{'d': 'e'}
```

### String Assertions

```python
from nimoy.specification import Specification

class MySpec(Specification):
    
    def string_assertion(self):
        with given:
            a = "There's a huge difference"
        with expect:
            a == "There's a small difference"
```

Produces

```
======================================================================
FAIL: string_assertion (builtins.MySpec)
----------------------------------------------------------------------
Traceback (most recent call last):
  [redacted]
AssertionError: 
Expected: "There's a small difference"
     but: was "There's a huge difference"
Hint:
- There's a huge difference
?           ^^^^

+ There's a small difference
?           ^^^^^
```

### Mock Assertions

```python
from nimoy.specification import Specification
from unittest import mock

class MySpec(Specification):
    
    def mock_assertion(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method()
        with then:
            2 * the_mock.some_method()
```

Produces

```
======================================================================
FAIL: mock_assertion (builtins.MySpec)
----------------------------------------------------------------------
Traceback (most recent call last):
  [redacted]
AssertionError: some_method was to be invoked 2 times but was invoked 1
```

## Stimulus and Response Specification

A specification with a `setup`, `when` and `then` block.

`when` blocks describe a certain action and `then` blocks assert the results of that action.

```python
from nimoy.specification import Specification

class MySpec(Specification):

    def my_feature_method(self):
        with setup:
            a = 1

        with when:
            a = a + 1

        with then:
            a == 2
```

## Expecting Exceptions

Use the `thrown` method to make sure that an expected exception has been thrown.

```python
from nimoy.specification import Specification

class MySpec(Specification):

    def my_feature_method(self):
        with when:
            raise Exception('Whaaaaat')
        with then:
            err = thrown(Exception)
            str(err[1]) == 'Whaaaaat'
```

## Data-driven Specification

Using the powerful `where` block, we can parametrise our specification and execute it multiple times with different sets of data.

### Data as a Matrix

We can set the parameters in the form of a matrix.

```python
from nimoy.specification import Specification

class MySpec(Specification):

    def my_feature_method(self):
        with given:
            a = value_of_a
            b = value_of_b

        with expect:
            (a * b) == expected_value

        with where:
            value_of_a | value_of_b | expected_value
            1          | 10         | 10
            2          | 20         | 40
```

### Data as a List

We can also set the parameters in the form of lists.

```python
from nimoy.specification import Specification

class MySpec(Specification):

    def my_feature_method(self):
        with given:
            a = value_of_a
            b = value_of_b

        with expect:
            (a * b) == expected_value

        with where:
            value_of_a = [1, 2]
            value_of_b = [10, 20]
            expected_value = [10, 40]
```

## Pretty Mock Response Staging

When using `unittest` mocks you can stage the return values using binary operators.

Use the right shift to always return the same value (`return_value`):

```python
from unittest import mock
from nimoy.specification import Specification

class MySpec(Specification):

    def my_feature_method(self):
        with setup:
            the_mock = mock.Mock()

        with when:
            the_mock.some_method() >> 5

        with then:
            the_mock.some_method() == 5
            the_mock.some_method() == 5
            the_mock.some_method() == 5
```

Or use the left shift operator to return a different value on every invocation (`side_effect`):

```python
from unittest import mock
from nimoy.specification import Specification

class MySpec(Specification):

    def my_feature_method(self):
        with setup:
            the_mock = mock.Mock()

        with when:
            the_mock.some_method() << [5, 6, 7]

        with then:
            the_mock.some_method() == 5
            the_mock.some_method() == 6
            the_mock.some_method() == 7
```

## Pretty Mock Assertions

When using `unittest` Mocks you can write pretty assertions in the `then` block.
Mock assertion expressions are written like a mathematical expression with the format of `[NUMBER_OF_INVOCATIONS] * [INVOCATION_TARGET]`.

`[NUMBER_OF_INVOCATIONS]` may be a wildcard when filled in with `\_`.

Invocation target arguments may also be wildcarded by placing `_`. For example, `class.method(_, 3)`.

```python
from unittest import mock
from nimoy.specification import Specification

class MySpec(Specification):

    def my_feature_method(self):
        with setup:
            the_mock = mock.Mock()

        with when:
            the_mock.some_method('abcd', True)

        with then:
            1 * the_mock.some_method('abcd', True)
```

## RegEx Matching

Use the `@` shorthand for pretty regex matching.

```python
import re

from nimoy.specification import Specification

class MySpec(Specification):

    def my_feature_method(self):
        with expect:
            'The quick brown fox' @ '.+brown.+' # This is valid regex matching!
            'The quick\nbrown fox' @ re.compile('.+brown.+', re.MULTILINE) # You can also provide your own pattern
```

## Skipping Features

You can use unittest's standard decorator to skip features.

```python
import unittest

from nimoy.specification import Specification

class MySpec(Specification):

    @unittest.skip
    def my_feature_method(self):
        with given:
            a = 'The quick brown fox'
        with expect:
            a == 'The quick frown box'
```