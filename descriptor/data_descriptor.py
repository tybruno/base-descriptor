""" Data Descriptor Module.

Data Descriptors are used to define how an attribute is set, retrieved,
and retrieved from an object.


A data descriptor in Python is a descriptor that implements at least one of
the following special methods: `__get__()`, `__set__()`, or `__delete__()`.
These methods allow you to customize attribute access and modification for
instances of a class.

Object Provided by this module:
    `AbstractDataDescriptor`: Abstract Base Class for Data Descriptors.
        Should be used when creating your own data descriptor.
    `BaseDataDescriptor`: Base Class for Data Descriptors which provides
        default behavior of standard class attributes.
        Can be used as a base class for your own data descriptor and
        override the necessary methods.
    `DefaultDataDescriptor`: Data Descriptor which provides an optional
        default value if no value is set.
    `ReadOnly`: Data Descriptor which is read only.

References:
    [1] Python Documentation. (n.d.). Descriptor HowTo Guide. Retrieved from
        https://docs.python.org/3/howto/descriptor.html
    [2] Dr. Fred Baptiste. (2023). Python Deep Dive: Part 4 [Online course].
        Udemy. Available at:
        https://www.udemy.com/course/python-3-deep-dive-part-4/
"""
import abc
from typing import Any, NoReturn, Optional, Type

# Globals
# Sentinel value for if default value is not set.
NO_DEFAULT = object()


class AbstractDataDescriptor(abc.ABC):
    """ Abstract Base Class for Data Descriptors.

    If an object defines `__set__()` or `__delete__()`, it is considered a data
    descriptor. `__get__()` and `__set_name__()`  are optional.
    """

    @abc.abstractmethod
    def __set__(
            self,
            instance: Any,
            value: Any,
    ):
        """ Set a value to the descriptor's attribute.

        Args:
            instance:  refers to the instance of the class on which the
                descriptor is accessed. When the attribute is set through an
                instance (e.g., my_instance.descriptor_attr = value), instance
                will be the instance of the class.
            value: The value to be set to the descriptor's attribute.
        """
        pass

    @abc.abstractmethod
    def __delete__(self, instance: Any):
        pass


class ReadOnly(AbstractDataDescriptor):
    """ Data Descriptor that is read only.

    Since `__set__()` is implemented, although it only raises an
    `AttributeError`, this is considered a data descriptor.

    Attributes:
        _value: The read only value to be returned when `__get__()` is called.
        _property_name: The name of the property.


    >>> class Person:
    ...     name = ReadOnly("Guido")
    >>> Person.name # doctest:+ELLIPSIS
    <data_descriptor.ReadOnly object at ...>
    >>> person = Person()
    >>> person.name
    'Guido'
    >>> person.name = "Raymond" # doctest:+ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: ...

    """

    def __init__(self, value: Any):
        AbstractDataDescriptor.__init__(self)
        self._value: Any = value

    def __set_name__(self, owner: Type, name: str):
        """ Allows the descriptor to know the name of the attribute to which
        it's being assigned.

        Args:
            owner: the class in which the descriptor is being assigned.
            name: the name of the attribute to which the descriptor is being
            assigned.
        """
        self._property_name = name

    def __get__(
            self,
            instance: Any,
            owner: Optional[Type] = None,
    ):
        """ Access the descriptor's attribute through an instance or a class.

        Args:
            instance: This parameter refers to the instance of the class on
                which the descriptor is accessed. When the attribute is
                accessed through an instance (e.g.,
                my_instance.descriptor_attr),
                instance will be the instance of the class.
            owner: This parameter refers to the class in which the descriptor
                is defined. When the attribute is accessed through the class (
                e.g., MyClass.descriptor_attr), owner will be the class.

        Returns:
            The read only value retrieved from the descriptor or the
            descriptor itself if called through the class.
        """
        if instance is None:
            return self

        return self._value

    def __set__(self, instance: Any, value: Any) -> NoReturn:
        """ If set is called raise `AttributeError` since readonly.

        Args:
            instance:  refers to the instance of the class on which the
                descriptor is accessed. When the attribute is set through an
                instance (e.g., my_instance.descriptor_attr = value), instance
                will be the instance of the class.
            value: The value that is attempted to be set to the descriptor's
                attribute.

        Raises:
            `AttributeError` if called through an instance.
        """
        raise AttributeError(
            f"{instance}.{self._property_name}", "is read only."
        )

    def __delete__(self, instance: Any) -> NoReturn:
        """ If delete is called raise `AttributeError` since readonly.

        Args:
            instance: the instance of the class on which the descriptor is
                accessed. When the attribute is deleted through an instance (
                e.g., del my_instance.attr), instance will be the instance of
                the class.

        Raises:
            `AttributeError` if called through an instance.
        """
        raise AttributeError(
            f"{instance}.{self._property_name}", "is not deletable."
        )


class BaseDataDescriptor(AbstractDataDescriptor):
    """ Provides the same functionality as a standard attribute.

    provides `__set_name__()`, `__set__()`, `__get__()`,
    and `__delete__()` implementation and can be overwritten by
    the child class to provide more functionality.

    Attributes:
        _property_name: The name of the property.

    Example:
        >>> class MyDescriptor(BaseDataDescriptor):
        ...     def __set__(self, instance, value):
        ...         print(f"Setting {self._property_name} to {value}")
        ...         instance.__dict__[self._property_name] = value
        >>> class Foo:
        ...     bar = MyDescriptor()
        >>> foo = Foo()
        >>> foo.bar = 1
        Setting bar to 1
        >>> foo.bar
        1
    """

    def __set_name__(self, owner: Type, name: Any):
        """ Allows the descriptor to know the name of the attribute to which
        it's being assigned.

        Args:
            owner: the class in which the descriptor is being assigned.
            name: the name of the attribute to which the descriptor is being
            assigned.
        """
        self._property_name = name

    def __set__(self, instance: Any, value: Any):
        """ Set a value to the descriptor's attribute.

        Args:
            instance:  refers to the instance of the class on which the
                descriptor is accessed. When the attribute is set through an
                instance (e.g., my_instance.descriptor_attr = value), instance
                will be the instance of the class.
            value: The value to be set to the descriptor's attribute.
        """
        instance.__dict__[self._property_name] = value

    def __get__(
            self,
            instance: Any,
            owner: Optional[Type] = None,
    ):
        """ Access the descriptor's attribute through an instance or a class.

        Args:
            instance: This parameter refers to the instance of the class on
                which the descriptor is accessed. When the attribute is
                accessed through an instance (e.g.,
                my_instance.descriptor_attr), instance will be the instance
                of the class.
            owner: This parameter refers to the class in which the descriptor
                is defined. When the attribute is accessed through the class (
                e.g., MyClass.descriptor_attr), owner will be the class.

        Returns:
            The value retrieved from the descriptor or the
            descriptor itself if called through the class.
        """
        if instance is None:
            return self
        try:
            return instance.__dict__[self._property_name]
        except KeyError:
            raise AttributeError(
                f"{instance}.{self._property_name}",
                "has not been set with a value"
            ) from None

    def __delete__(self, instance: Any) -> NoReturn:
        """ If delete is called raise `AttributeError` since readonly.

        Args:
            instance: the instance of the class on which the descriptor is
                accessed. When the attribute is deleted through an instance (
                e.g., del my_instance.attr), instance will be the instance of
                the class.

        Raises:
            `AttributeError` if called through an instance.
        """
        raise AttributeError(
            f"{instance}.{self._property_name}", "is not deletable."
        )


class DefaultDescriptor(BaseDataDescriptor):
    """ Data Descriptor that provides a default value.

    An optional default value can be set for the descriptor.

    Attributes:
        default: The default value to be returned when `__get__()` is called
        and no value has been set.
        _property_name: The name of the property.

    Example:
        >>> class Foo:
        ...     bar = DefaultDescriptor(default=1)
        >>> foo = Foo()
        >>> foo.bar
        1
        >>> foo.bar = 2
        >>> foo.bar
        2
    """

    def __init__(
            self, *,
            default: Optional[Any] = NO_DEFAULT
    ):
        self.default: Optional[Any] = default

    def __get__(
            self, instance: Any,
            owner: Optional[Type] = None
    ) -> Any:
        """ Access the descriptor's attribute through an instance or a class.

        Args:
            instance: This parameter refers to the instance of the class on
                which the descriptor is accessed. When the attribute is
                accessed through an instance (e.g.,
                my_instance.descriptor_attr), instance will be the instance
                of the class.
            owner: This parameter refers to the class in which the descriptor
                is defined. When the attribute is accessed through the class (
                e.g., MyClass.descriptor_attr), owner will be the class.

        Returns:
            The Value retrieved from the descriptor, default, or the
            descriptor itself if called through the class.
        """

        if instance is None:
            return self

        _default: Any = self.default

        if _default is NO_DEFAULT:
            value = BaseDataDescriptor.__get__(self, instance, owner)
            return value

        value = instance.__dict__.get(self._property_name, _default)
        return value
