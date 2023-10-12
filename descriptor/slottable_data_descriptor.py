""" Slottable Data Descriptor Module

The slottable data descriptor has the following advantages:
1. Has instance specific storage
2. Does not use the instance for storage, thus works with __slots__.
    `__slots__ = "__weakref__"` must be set.
3. Handles non hashable instances
4. Data storage is clean.



Objects defined in the module:
    `Reference`: `NamedTuple` Used in Slottable Data Descriptors to
        Reference an instance and its value.
    `BaseSlottableDataDescriptor`: Base class for making Slottable Data
        Descriptors.
    `SlottableDefaultDataDescriptor`: Slottable Data Descriptor with default
        value.


References:
    [1] Dr. Fred Baptiste. (2023). Python Deep Dive: Part 4 [Online course].
        Udemy. Available at:
        https://www.udemy.com/course/python-3-deep-dive-part-4/
"""
from typing import NamedTuple, Type, Optional, Dict, Any, NoReturn
import weakref
from descriptor import data_descriptor

# Globals
# Sentinel value to indicate no default value was provided.
NO_DEFAULT = data_descriptor.NO_DEFAULT


class Reference(NamedTuple):
    """ Used in Slottable Data Descriptors to Reference an instance and its
    value.

    Attributes:
        reference: Weak reference to an instance.
        value: The value of the instance.
    """
    reference: weakref.ref
    value: Any


class BaseSlottableDataDescriptor(data_descriptor.AbstractDataDescriptor):
    """ Base class for making Slottable Data Descriptors.

    The slottable data descriptor have the following advantages:
    1. Has instance specific storage.
    2. Does not use the instance for storage, thus works with __slots__.
        Make sure __slots__ = "__weakref__".
    3. Handles non hashable instances.
    4. Data storage is clean.



    Note:
        Must Include `__slots__ = "__weakref__"` to make the class work the
        slottable data descriptor.

    Attributes:
        _references: `typing.Dict[int, Reference]` Dictionary of references
        to instances and their values.

    Example:
        >>> class Person:
        ...     __slots__ = "__weakref__"
        ...     first_name = BaseSlottableDataDescriptor()
        >>> Person.first_name # doctest:+ELLIPSIS
        <slottable_data_descriptor.BaseSlottableDataDescriptor object at ...>
        >>> person = Person()
        >>> person.first_name = "Raymond"
        >>> person.first_name
        'Raymond'
        >>> person.__dict__ # doctest:+ELLIPSIS
        Traceback (most recent call last):
        ...
        AttributeError: ...
        >>> person.__slots__
        '__weakref__'

    References:
        [1] Dr. Fred Baptiste. (2023). Python Deep Dive: Part 4 [Online
            course]. Udemy. Available at:
            https://www.udemy.com/course/python-3-deep-dive-part-4/
    """

    def __init__(self):
        self._references: Dict[int, Reference] = {}

    def __set_name__(self, owner: Type, name: str):
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
        _weak_ref: weakref.ref = weakref.ref(instance, self._delete_reference)
        reference: Reference = Reference(_weak_ref, value)
        _instance_id = id(instance)
        self._references[_instance_id] = reference

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
            The Value retrieved from the descriptor or the
            descriptor itself if called through the class.
        """
        if instance is None:
            return self
        _instance_id = id(instance)
        try:
            _reference: Reference = self._references[_instance_id]
            value: Any = _reference.value
            return value
        except KeyError:
            raise AttributeError(
                f"{instance}.{self._property_name}",
                "has not been set with a value."
            ) from None

    def __delete__(self, instance: Any) -> NoReturn:
        raise AttributeError(
            f"{instance}.{self._property_name}", "is not deletable."
        )

    def _find_weak_ref_key(self, weak_ref: weakref.ref) -> Any:
        """ Find the key in the references dictionary that matches the weak
        reference.

        Args:
            weak_ref: Weak reference to an instance.

        Returns:
            `typing.Any` The key in the references dictionary that matches
            the weak reference.
        """
        for key, reference in self._references.items():
            if reference.reference is weak_ref:
                return key

    def _delete_reference(self, weak_ref: weakref.ref) -> None:
        """ Delete the reference to the instance from the references
        dictionary.

        Args:
            weak_ref: Weak reference to an instance.
        """
        key = self._find_weak_ref_key(weak_ref)
        if key:
            del self._references[key]


class SlottableDefaultDescriptor(BaseSlottableDataDescriptor):
    """ Slottable Data Descriptor with a default value.

    The slottable data descriptor have the following advantages:
    1. Has instance specific storage
    2. Does not use the instance for storage, thus works with __slots__.
    Make sure __slots__ = ("__weakref__", )
    3. Handles non hashable instances
    4. Data storage is clean.

    Must Include `__slots__ = "__weakref__"` to make the class work the
    slottable data descriptor.

    Attributes:
        _references: `typing.Dict[int, Reference]` Dictionary of references
        to instances and their values.
        default: `typing.Any` The default value to use if no value has been
        set.

    Example:
        >>> class Person:
        ...     __slots__ = "__weakref__"
        ...     first_name = SlottableDefaultDescriptor(default="Raymond")
        >>> Person.first_name # doctest:+ELLIPSIS
        <slottable_data_descriptor.SlottableDefaultDescriptor object at ...>
        >>> person = Person()
        >>> person.first_name
        'Raymond'
        >>> person.first_name = 'Guido'
        >>> person.first_name
        'Guido'
        >>> person.__dict__ # doctest:+ELLIPSIS
        Traceback (most recent call last):
        ...
        AttributeError: ...
        >>> person.__slots__
        '__weakref__'
    """

    def __init__(self, *, default: Any = NO_DEFAULT):
        BaseSlottableDataDescriptor.__init__(self)
        self.default = default

    def __get__(
            self, instance: Any,
            owner: Optional[Type] = None
    ) -> Any:
        """ Access the descriptor's attribute through an instance or a class.

        Args:
            instance: This parameter refers to the instance of the class on
                which the descriptor is accessed. When the attribute is
                accessed through an instance (e.g.,
                my_instance.descriptor_attr),instance will be the instance
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

        _default = self.default

        if _default is NO_DEFAULT:
            value = BaseSlottableDataDescriptor.__get__(self, instance, owner)
            return value

        _instance_id = id(instance)
        _value_or_reference = self._references.get(
            _instance_id, _default
        )

        if isinstance(_value_or_reference, Reference):
            value = _value_or_reference.value
        else:
            value = _value_or_reference

        return value
