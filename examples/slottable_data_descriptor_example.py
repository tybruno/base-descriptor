from base_descriptor import (
    BaseSlottableDataDescriptor,
    SlottableDefaultDescriptor,
)


def slottable_default_data_descriptor_example():
    """ This example shows how to use the `SlottableDefaultDataDescriptor`
    class."""

    class Person:
        __slots__ = "__weakref__"
        first_name = SlottableDefaultDescriptor(
            default="Guido"
        )

    person = Person()
    print(person.first_name)  # Guido
    person.first_name = "Raymond"
    print(person.first_name)  # Raymond


def base_slottable_data_descriptor_example():
    """ This example shows how to use the `BaseSlottableDataDescriptor`
    class. """

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


if __name__ == "__main__":
    slottable_default_data_descriptor_example()
    base_slottable_data_descriptor_example()
