[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![License: MIT](https://img.shields.io/badge/License-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/tybruno/descriptor/branch/main/graph/badge.svg?token=j6pZAXF6cw)](https://codecov.io/gh/tybruno/descriptor)

# base-descriptor

A simple, fast, typed, and tested abstract and base classes for a python3.6+
Non Data Descriptor, Data Descriptor, and Slottable Data Descriptor. The goal
is to
aid in the creation of descriptors allowing other developers to make
descriptors for their own use case.

#### Key Features:

* **Easy**: Flexable and easy to inherit the prebuilt Non Data Descriptors,
  Data Descriptors, and Slottable Data Descriptors to create your own
  descriptors.
* **Great Developer Experience**: Being fully typed makes it great for editor
  support.
* **Fully Tested**: Our test suit fully tests the functionality to ensure that
  all of the classes in this module run as expected.

## Installation

`pip install base-descriptor`

## Table of Contents

- [Objects Provided in this Module](#objects-provided-in-this-module)
    - [Non Data Descriptors](#non-data-descriptors)
    - [Data Descriptors](#data-descriptors)
    - [Slottable Data Descriptors](#slottable-data-descriptors)
- [Non Data Descriptor Examples](#non-data-descriptor-examples)
    - [AbstractNonDataDescriptor](#abstractnondatadescriptor)
- [Data Descriptor Examples](#data-descriptor-examples)
    - [ReadOnly](#readonly)
    - [DefaultDescriptor](#defaultdescriptor)
    - [BaseDataDescriptor](#basedatadescriptor)
    - [AbstractDataDescriptor](#abstractdatadescriptor)
- [Slottable Data Descriptors](#slottable-data-descriptors-1)
    - [SlottableDefaultDescriptor](#slottabledefaultdescriptor)
    - [BaseSlottableDataDescriptor](#baseslottabledatadescriptor)
- [References](#references)

## Objects Provided in this Module

### Non Data Descriptors

A non-data descriptor in Python is a type of descriptor that only implements
the `__get__()` method. Descriptors are a way to customize attribute access in
Python. When an attribute is
accessed on an object, Python checks if a descriptor exists for that attribute
in the class or its ancestors. If found, the descriptor's `__get__()` method is
called to determine the final
value of the attribute.

| Class                       | Description                                            |
|-----------------------------|--------------------------------------------------------|
| `AbstractNonDataDescriptor` | Abstract Base Class for creating Non Data Descriptors. |

### Data Descriptors

A data descriptor in Python is a type of descriptor that implements
both `__get__()` and either `__set__()` or `__delete__()`. Data descriptors
allow you to define custom behavior for
attribute
access, including setting or deleting the attribute in addition to retrieving
its value.

| Class                    | Description                                                                                        |
|--------------------------|----------------------------------------------------------------------------------------------------|
| `AbstractDataDescriptor` | Abstract Base Class for creating Data Descriptors.                                                 |
| `BaseDataDescriptor`     | Base Class for creating Data Descriptors. Provides the same functionality as a standard attribute. | 
| `DefaultDescriptor`      | A Data Descriptor that has a default value.                                                        |
| `ReadOnly`               | A Data Descriptor that is read only.                                                               |

### Slottable Data Descriptors

A Data Descriptor that plays well with `__slots__`. This module was inspired by
Dr. Fred Baptiste [fbaptiste](https://github.com/fbaptiste).

The slottable data descriptor has the following advantages:

1. Has instance specific storage
2. Does not use the instance for storage, thus works with __slots__.
   `__slots__ = "__weakref__"` must be set.
3. Handles non hashable instances
4. Data storage is clean.

| Class                             | Description                                                                                                  |
|-----------------------------------|--------------------------------------------------------------------------------------------------------------|
| `AbstractSlottableDataDescriptor` | Abstract Base Class for creating Slottable Data Descriptors.                                                 |
| `BaseSlottableDataDescriptor`     | Base Class for creating Slottable Data Descriptors. Provides the same functionality as a standard attribute. |
| `SlottableDefaultDescriptor`      | A Slottable Data Descriptor that has a default value.                                                        |

## Non Data Descriptor Examples

### `AbstractNonDataDescriptor`

Simple way to Inherit from `AbstractNonDataDescriptor` to create your own Non
Data Descriptor.

```python
from base_descriptor import AbstractNonDataDescriptor


class SquareDescriptor(AbstractNonDataDescriptor):
    def __get__(self, instance, owner=None):
        if instance is None:
            # Access through the class, return the descriptor itself
            return self
        return instance._value ** 2


class MyClass:
    square = SquareDescriptor()

    def __init__(self, value):
        self._value = value


# Create an instance of MyClass
my_instance = MyClass(5)

# Access the square attribute using the descriptor
# This will calculate and return the square
print(my_instance.square)  # 25
```

## Data Descriptor Examples

### `ReadOnly`

```python
from base_descriptor import ReadOnly


class Person:
    name = ReadOnly("Guido")


person = Person()
print(person.name)  # Guido
person.name = "Raymond"  # raises AttributeError
```

### `DefaultDescriptor`

Default Descriptor that provides a default value for the attribute.

```python
from base_descriptor import DefaultDescriptor


class Person:
    name = DefaultDescriptor(default="Guido")


print(Person.name)  # <data_descriptor.DefaultDescriptor object at ...>
person = Person()
print(person.name)  # Guido
person.name = "Raymond"
print(person.name)  # Raymond
```

### `BaseDataDescriptor`

Provides the same functionality as a standard attribute.
It enables you to create your own Data Descriptor by overriding
the `__set_name__()`, `__set__()`, `__get__()`,
or `__delete__()` methods to match your requirements.

```python
from base_descriptor import BaseDataDescriptor


class Plus2(BaseDataDescriptor):
    def __set__(self, instance, value):
        value = value + 2
        instance.__dict__[self._property_name] = value


class Foo:
    bar = Plus2()


foo = Foo()
foo.bar = 1
print(foo.bar)  # 3
```

### `AbstractDataDescriptor`

Provides an Abstract Base Class that can be inherited from to help create your
own Data Descriptors.

```python
from base_descriptor import AbstractDataDescriptor


class MyDataDescriptor(AbstractDataDescriptor):
    def __init__(self):
        self._value = None

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        self._value = value

    def __delete__(self, instance):
        self._value = None


class MyClass:
    my_data_descriptor = MyDataDescriptor()


obj = MyClass()
obj.my_data_descriptor = 1
print(obj.my_data_descriptor)  # 1
```

## Slottable Data Descriptors

### `SlottableDefaultDescriptor`

Slottable Default Descriptor that provides a default value for the attribute.

```python
from base_descriptor import SlottableDefaultDescriptor


class Person:
    __slots__ = "__weakref__"
    first_name = SlottableDefaultDescriptor(default="Guido")


person = Person()
print(person.first_name)  # Guido
person.first_name = "Raymond"
print(person.first_name)  # Raymond
```

### `BaseSlottableDataDescriptor`

Provides the same functionality as a standard attribute.
It enables you to create your own Slottable Data Descriptor by overriding
the `__set_name__()`, `__set__()`, `__get__()`,
or `__delete__()` methods to match your requirements.

```python
from base_descriptor import BaseSlottableDataDescriptor


class MyDescriptor(BaseSlottableDataDescriptor):
    def __set__(self, instance, value):
        print(f"Setting {self._property_name} to {value}")
        instance.__dict__[self._property_name] = value


class Foo:
    __slots__ = "__weakref__"
    bar = MyDescriptor()


foo = Foo()
foo.bar = 1
print(foo.bar)  # 1
```

## References

This module was heavily inspired by the following resources:

1. **Python Deep Dive: Part 4**
    - Author: Dr. Fred Baptiste ([fbaptiste](https://github.com/fbaptiste))
    - Year: 2023
    - Course
      Title: [Python Deep Dive: Part 4](https://www.udemy.com/course/python-3-deep-dive-part-4/)
    - Platform: Udemy

2. **Descriptor HowTo Guide**
    - Source: Python Documentation
    - URL:
      [Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)


