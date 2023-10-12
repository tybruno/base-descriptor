from descriptor import AbstractNonDataDescriptor


def abstract_non_data_descriptor_example():
    """This example shows how to use inherit the abstract base class
    `AbstractNonDataDescriptor`to create your own NonData Descriptors."""

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


if __name__ == "__main__":
    abstract_non_data_descriptor_example()
