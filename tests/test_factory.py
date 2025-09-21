"""Tests for DataStructureFactory."""

import pytest

from aste.datastructures.base import DataStructureBuilder
from aste.datastructures.builders import AttrsBuilder
from aste.datastructures.builders import DataclassBuilder
from aste.datastructures.builders import NamedTupleBuilder
from aste.datastructures.builders import PydanticBuilder
from aste.datastructures.builders import TypedDictBuilder
from aste.datastructures.factory import DataStructureFactory


class TestDataStructureFactory:
    """Test factory pattern for builder instantiation."""

    def test_get_typed_dict_builder(self) -> None:
        """Factory returns TypedDictBuilder."""
        builder = DataStructureFactory.get_builder("typed_dict")
        assert isinstance(builder, TypedDictBuilder)

    def test_get_dataclass_builder(self) -> None:
        """Factory returns DataclassBuilder."""
        builder = DataStructureFactory.get_builder("dataclass")
        assert isinstance(builder, DataclassBuilder)

    def test_get_pydantic_builder(self) -> None:
        """Factory returns PydanticBuilder."""
        builder = DataStructureFactory.get_builder("pydantic")
        assert isinstance(builder, PydanticBuilder)

    def test_get_namedtuple_builder(self) -> None:
        """Factory returns NamedTupleBuilder."""
        builder = DataStructureFactory.get_builder("namedtuple")
        assert isinstance(builder, NamedTupleBuilder)

    def test_get_attrs_builder(self) -> None:
        """Factory returns AttrsBuilder."""
        builder = DataStructureFactory.get_builder("attrs")
        assert isinstance(builder, AttrsBuilder)

    def test_unknown_builder_raises_error(self) -> None:
        """Factory raises ValueError for unknown builder type."""
        with pytest.raises(ValueError, match="Unknown builder type: invalid"):
            DataStructureFactory.get_builder("invalid")

    def test_all_builders_are_data_structure_builders(self) -> None:
        """All factory builders inherit from DataStructureBuilder."""
        builder_types = [
            "typed_dict",
            "dataclass",
            "pydantic",
            "namedtuple",
            "attrs",
        ]
        for builder_type in builder_types:
            builder = DataStructureFactory.get_builder(builder_type)
            assert isinstance(builder, DataStructureBuilder)

    def test_factory_returns_working_builders(self) -> None:
        """All factory builders can generate code."""
        builder_types = [
            "typed_dict",
            "dataclass",
            "pydantic",
            "namedtuple",
            "attrs",
        ]
        fields = {"id": "int", "name": "str"}

        for builder_type in builder_types:
            builder = DataStructureFactory.get_builder(builder_type)
            code = builder.build("TestModel", fields)

            # Basic validation
            assert "TestModel" in code
            assert "id: int" in code
            assert "name: str" in code
