from abstract_descriptor import ReadOnly, BaseDataDescriptor, DefaultDescriptor


def read_only_example():
    """ This example shows how to use the `ReadOnly` class."""

    class Person:
        name = ReadOnly("Guido")

    person = Person()
    print(person.name)  # Guido
    person.name = "Raymond"  # raises AttributeError


def default_data_descriptor_example():
    """ This example shows how to use the `DefaultDataDescriptor` class."""

    class Person:
        name = DefaultDescriptor(default="Guido")

    print(Person.name)  # <data_descriptor.DefaultDescriptor object at ...>
    person = Person()
    print(person.name)  # Guido
    person.name = "Raymond"
    print(person.name)  # Raymond


def base_data_descriptor_example():
    """ This example shows how to use the `BaseDataDescriptor` class to
    create your own descriptors."""

    class Plus2(BaseDataDescriptor):
        def __set__(self, instance, value):
            value = value + 2
            instance.__dict__[self._property_name] = value

    class Foo:
        bar = Plus2()

    foo = Foo()
    foo.bar = 1
    print(foo.bar)  # 3


if __name__ == "__main__":
    default_data_descriptor_example()
    base_data_descriptor_example()
    read_only_example()
