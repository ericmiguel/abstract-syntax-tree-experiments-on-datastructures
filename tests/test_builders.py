"""Tests for data structure builders."""

import ast

import pytest

from aste.datastructures.builders import AttrsBuilder
from aste.datastructures.builders import DataclassBuilder
from aste.datastructures.builders import NamedTupleBuilder
from aste.datastructures.builders import PydanticBuilder
from aste.datastructures.builders import TypedDictBuilder


class TestTypedDictBuilder:
    """Test TypedDict code generation."""

    def test_build_simple_typed_dict(self) -> None:
        """Generate simple TypedDict."""
        builder = TypedDictBuilder()
        code = builder.build("User", {"id": "int", "name": "str"})

        assert "from typing import TypedDict" in code
        assert "class User(TypedDict):" in code
        assert "id: int" in code
        assert "name: str" in code

    def test_build_empty_typed_dict(self) -> None:
        """Generate TypedDict with no fields."""
        builder = TypedDictBuilder()
        code = builder.build("Empty", {})

        assert "class Empty(TypedDict):" in code
        assert "pass" in code

    def test_generated_code_is_valid_python(self) -> None:
        """Generated code is valid Python AST."""
        builder = TypedDictBuilder()
        code = builder.build("User", {"id": "int"})

        # Should parse without errors
        ast.parse(code)


class TestDataclassBuilder:
    """Test dataclass code generation."""

    def test_build_simple_dataclass(self) -> None:
        """Generate simple dataclass."""
        builder = DataclassBuilder()
        code = builder.build("User", {"id": "int", "name": "str"})

        assert "from dataclasses import dataclass" in code
        assert "@dataclass" in code
        assert "class User:" in code
        assert "id: int" in code
        assert "name: str" in code

    def test_build_empty_dataclass(self) -> None:
        """Generate dataclass with no fields."""
        builder = DataclassBuilder()
        code = builder.build("Empty", {})

        assert "@dataclass" in code
        assert "class Empty:" in code
        assert "pass" in code

    def test_generated_code_is_valid_python(self) -> None:
        """Generated code is valid Python AST."""
        builder = DataclassBuilder()
        code = builder.build("User", {"id": "int", "active": "bool"})

        # Should parse without errors
        ast.parse(code)


class TestPydanticBuilder:
    """Test Pydantic BaseModel code generation."""

    def test_build_simple_model(self) -> None:
        """Generate simple Pydantic model."""
        builder = PydanticBuilder()
        code = builder.build("User", {"id": "int", "email": "str"})

        assert "from pydantic import BaseModel" in code
        assert "class User(BaseModel):" in code
        assert "id: int" in code
        assert "email: str" in code

    def test_build_empty_model(self) -> None:
        """Generate Pydantic model with no fields."""
        builder = PydanticBuilder()
        code = builder.build("Empty", {})

        assert "class Empty(BaseModel):" in code
        assert "pass" in code

    def test_generated_code_is_valid_python(self) -> None:
        """Generated code is valid Python AST."""
        builder = PydanticBuilder()
        code = builder.build("User", {"id": "int"})

        # Should parse without errors
        ast.parse(code)


class TestNamedTupleBuilder:
    """Test NamedTuple code generation."""

    def test_build_simple_namedtuple(self) -> None:
        """Generate simple NamedTuple."""
        builder = NamedTupleBuilder()
        code = builder.build("Point", {"x": "int", "y": "int"})

        assert "from typing import NamedTuple" in code
        assert "class Point(NamedTuple):" in code
        assert "x: int" in code
        assert "y: int" in code

    def test_generated_code_is_valid_python(self) -> None:
        """Generated code is valid Python AST."""
        builder = NamedTupleBuilder()
        code = builder.build("Point", {"x": "float", "y": "float"})

        # Should parse without errors
        ast.parse(code)


class TestAttrsBuilder:
    """Test attrs code generation."""

    def test_build_simple_attrs_class(self) -> None:
        """Generate simple attrs class."""
        builder = AttrsBuilder()
        code = builder.build("User", {"id": "int", "name": "str"})

        assert "from attr import define" in code
        assert "@define" in code
        assert "class User:" in code
        assert "id: int" in code
        assert "name: str" in code

    def test_generated_code_is_valid_python(self) -> None:
        """Generated code is valid Python AST."""
        builder = AttrsBuilder()
        code = builder.build("Config", {"debug": "bool"})

        # Should parse without errors
        ast.parse(code)


class TestBuilderFieldTypes:
    """Test builders handle various field types correctly."""

    @pytest.mark.parametrize(
        "builder_class",
        [
            TypedDictBuilder,
            DataclassBuilder,
            PydanticBuilder,
            NamedTupleBuilder,
            AttrsBuilder,
        ],
    )
    def test_multiple_field_types(self, builder_class: type) -> None:
        """All builders handle multiple field types."""
        builder = builder_class()
        fields = {
            "id": "int",
            "name": "str",
            "active": "bool",
            "score": "float",
            "tags": "list[str]",
            "metadata": "dict[str, Any]",
        }
        code = builder.build("ComplexModel", fields)

        # Verify all fields present
        for field_name, field_type in fields.items():
            assert f"{field_name}: {field_type}" in code

        # Verify valid Python
        ast.parse(code)
