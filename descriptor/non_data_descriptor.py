""" Non Data Descriptor Module

Non Data Descriptors are descriptors that implement `__get__()`.
Optionally `__set_name__()` can be set. This means that while they can
customize the behavior of attribute access (getting), they do not control
setting or deleting the attribute.

Objects provided by this module:
    `AbstractNonDataDescriptor`: Abstract Base Class for Non Data Descriptors.
        Used for creating your own non-data descriptors.

References:
    [1] Python Documentation. (n.d.). Descriptor HowTo Guide. Retrieved from
        https://docs.python.org/3/howto/descriptor.html
    [2] Dr. Fred Baptiste. (2023). Python Deep Dive: Part 4 [Online course].
        Udemy. Available at:
        https://www.udemy.com/course/python-3-deep-dive-part-4/
"""
import abc
from typing import Any, Optional, Type


class AbstractNonDataDescriptor(abc.ABC):
    """ Abstract Base Class for Non Data Descriptors.

    Non-data descriptors must implement `__get__`. `__set_name__` is optional.
    """

    @abc.abstractmethod
    def __get__(
            self, instance: Any,
            owner: Optional[Type] = None
    ):
        """ Access the descriptor's attribute through an instance or a class.

        Args:
            instance: This parameter refers to the instance of the class on
                which the descriptor is accessed. When the attribute is
                accessed through an instance (e.g.,
                my_instance.descriptor_attr), instance will be the instance
                of the class.
            owner: This parameter refers to the class in which the descriptor
                is defined. When the attribute is accessed through the class
                (e.g., MyClass.descriptor_attr), owner will be the class.
        """
        pass
