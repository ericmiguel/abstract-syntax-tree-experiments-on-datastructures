"""Tests for JSON schema inference utilities."""

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from aste.utils.json_schema import infer_fields_from_json
from aste.utils.json_schema import infer_python_type
from aste.utils.json_schema import load_json_from_file


class TestInferPythonType:
    """Test type inference from Python values."""

    def test_infer_none(self) -> None:
        """Infer None type."""
        assert infer_python_type(None) == "None"

    def test_infer_bool(self) -> None:
        """Infer bool type."""
        assert infer_python_type(True) == "bool"
        assert infer_python_type(False) == "bool"

    def test_infer_int(self) -> None:
        """Infer int type."""
        assert infer_python_type(42) == "int"
        assert infer_python_type(-100) == "int"
        assert infer_python_type(0) == "int"

    def test_infer_float(self) -> None:
        """Infer float type."""
        assert infer_python_type(3.14) == "float"
        assert infer_python_type(-2.5) == "float"
        assert infer_python_type(0.0) == "float"

    def test_infer_str(self) -> None:
        """Infer str type."""
        assert infer_python_type("hello") == "str"
        assert infer_python_type("") == "str"

    def test_infer_empty_list(self) -> None:
        """Infer list type from empty list."""
        assert infer_python_type([]) == "list[Any]"

    def test_infer_list_of_int(self) -> None:
        """Infer list[int] type."""
        assert infer_python_type([1, 2, 3]) == "list[int]"

    def test_infer_list_of_str(self) -> None:
        """Infer list[str] type."""
        assert infer_python_type(["a", "b", "c"]) == "list[str]"

    def test_infer_empty_dict(self) -> None:
        """Infer dict type from empty dict."""
        assert infer_python_type({}) == "dict[str, Any]"

    def test_infer_dict_str_int(self) -> None:
        """Infer dict[str, int] type."""
        assert infer_python_type({"a": 1, "b": 2}) == "dict[str, int]"

    def test_infer_dict_str_str(self) -> None:
        """Infer dict[str, str] type."""
        assert infer_python_type({"name": "Alice", "city": "NYC"}) == "dict[str, str]"

    def test_infer_nested_list(self) -> None:
        """Infer nested list type."""
        assert infer_python_type([[1, 2], [3, 4]]) == "list[list[int]]"

    def test_infer_unknown_type(self) -> None:
        """Infer Any for unknown types."""
        assert infer_python_type(object()) == "Any"


class TestLoadJsonFromFile:
    """Test loading JSON from local files."""

    def test_load_valid_json(self) -> None:
        """Load valid JSON from file."""
        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"name": "Alice", "age": 30}, f)
            temp_path = Path(f.name)

        try:
            data = load_json_from_file(temp_path)
            assert data == {"name": "Alice", "age": 30}
        finally:
            temp_path.unlink()

    def test_load_nonexistent_file(self) -> None:
        """Raise FileNotFoundError for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            load_json_from_file("nonexistent.json")

    def test_load_invalid_json(self) -> None:
        """Raise JSONDecodeError for invalid JSON."""
        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not valid json {")
            temp_path = Path(f.name)

        try:
            with pytest.raises(json.JSONDecodeError):
                load_json_from_file(temp_path)
        finally:
            temp_path.unlink()


class TestInferFieldsFromJson:
    """Test field inference from JSON data."""

    def test_infer_simple_fields(self) -> None:
        """Infer fields from simple JSON."""
        data = {
            "user_id": 123,
            "username": "alice",
            "is_active": True,
        }
        fields = infer_fields_from_json(data)
        assert fields == {
            "user_id": "int",
            "username": "str",
            "is_active": "bool",
        }

    def test_infer_mixed_fields(self) -> None:
        """Infer fields with various types."""
        data = {
            "id": 1,
            "name": "Product",
            "price": 99.99,
            "tags": ["electronics", "gadget"],
            "metadata": {"color": "black", "size": "medium"},
        }
        fields = infer_fields_from_json(data)
        assert fields["id"] == "int"
        assert fields["name"] == "str"
        assert fields["price"] == "float"
        assert fields["tags"] == "list[str]"
        assert fields["metadata"] == "dict[str, str]"

    def test_infer_empty_json(self) -> None:
        """Infer fields from empty JSON."""
        fields = infer_fields_from_json({})
        assert fields == {}
