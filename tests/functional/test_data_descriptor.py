import pytest

import base_descriptor


@pytest.fixture(
    params=[base_descriptor.SlottableDefaultDescriptor,
            base_descriptor.DefaultDescriptor],
    ids=["SlottableDefaultDataDescriptor", "DefaultDataDescriptor"],
)
def default_data_descriptor(request):
    return request.param


@pytest.fixture(
    params=[base_descriptor.BaseSlottableDataDescriptor,
            base_descriptor.BaseDataDescriptor],
    ids=["BaseSlottableDataDescriptor", "BaseDataDescriptor"],
)
def base_data_descriptor(request):
    return request.param


class TestBaseDescriptor:
    def test_base_descriptor(self, base_data_descriptor):
        _descriptor = base_data_descriptor()

        class Person:
            first_name = _descriptor

        assert Person.first_name == _descriptor

        person = Person()
        with pytest.raises(AttributeError):
            person.first_name
        person.first_name = "Guido"
        assert person.first_name == "Guido"

        with pytest.raises(AttributeError):
            del person.first_name


class TestDefaultDescriptor:
    def test_default_descriptor_default_set(self, default_data_descriptor):
        _descriptor = default_data_descriptor(default="Raymond")

        class Person:
            first_name = _descriptor

        assert Person.first_name == _descriptor
        person = Person()
        assert person.first_name == "Raymond"
        person.first_name = "Guido"
        assert person.first_name == "Guido"

    def test_default_descriptor_default_not_set(self, default_data_descriptor):
        _descriptor = default_data_descriptor()

        class Person:
            first_name = _descriptor

        assert Person.first_name == _descriptor

        person = Person()
        with pytest.raises(AttributeError):
            person.first_name
        person.first_name = "Guido"
        assert person.first_name == "Guido"


class TestReadOnly:
    def test_read_only(self):
        _descriptor = base_descriptor.ReadOnly(1)

        class A:
            x: int = _descriptor

        assert A.x == _descriptor
        a = A()
        assert a.x == 1
        with pytest.raises(AttributeError):
            a.x = 2

        with pytest.raises(AttributeError):
            del a.x
