"""JSON schema inference utilities."""

import json
from pathlib import Path
from typing import Any
from urllib.request import urlopen


def load_json_from_file(file_path: str | Path) -> dict[str, Any]:
    """
    Load JSON data from a local file.

    Parameters
    ----------
    file_path : str | Path
        Path to the JSON file

    Returns
    -------
    dict[str, Any]
        Parsed JSON data

    Raises
    ------
    FileNotFoundError
        If the file does not exist
    json.JSONDecodeError
        If the file contains invalid JSON

    Examples
    --------
    >>> data = load_json_from_file("user.json")
    >>> isinstance(data, dict)
    True
    """
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_json_from_url(url: str) -> dict[str, Any]:
    """
    Load JSON data from a URL.

    Parameters
    ----------
    url : str
        URL to fetch JSON from

    Returns
    -------
    dict[str, Any]
        Parsed JSON data

    Raises
    ------
    urllib.error.URLError
        If the URL cannot be reached
    json.JSONDecodeError
        If the response contains invalid JSON

    Examples
    --------
    >>> data = load_json_from_url("https://api.example.com/user/123")
    >>> isinstance(data, dict)
    True
    """
    with urlopen(url) as response:
        content = response.read().decode("utf-8")
        return json.loads(content)


def infer_python_type(value: Any) -> str:  # noqa: C901
    """
    Infer Python type annotation from a value.

    Parameters
    ----------
    value : Any
        Value to infer type from

    Returns
    -------
    str
        Python type annotation as string

    Examples
    --------
    >>> infer_python_type(42)
    'int'
    >>> infer_python_type("hello")
    'str'
    >>> infer_python_type([1, 2, 3])
    'list[int]'
    >>> infer_python_type({"a": 1})
    'dict[str, int]'
    """
    if value is None:
        return "None"
    elif isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "str"
    elif isinstance(value, list):
        if not value:
            return "list[Any]"
        # Infer type from first element
        first_type = infer_python_type(value[0])
        return f"list[{first_type}]"
    elif isinstance(value, dict):
        if not value:
            return "dict[str, Any]"
        # Infer from first key-value pair - use type: ignore for dynamic dict
        items: list[tuple[Any, Any]] = list(value.items())  # type: ignore[misc]
        if items:
            first_key: Any
            first_value: Any
            first_key, first_value = items[0]
            key_type = infer_python_type(first_key)
            value_type = infer_python_type(first_value)
            return f"dict[{key_type}, {value_type}]"
        return "dict[str, Any]"
    else:
        return "Any"


def infer_fields_from_json(data: dict[str, Any]) -> dict[str, str]:
    """
    Infer field types from JSON data structure.

    Parameters
    ----------
    data : dict[str, Any]
        JSON data to analyze

    Returns
    -------
    dict[str, str]
        Mapping of field names to Python type annotations

    Examples
    --------
    >>> data = {"user_id": 123, "username": "ada", "is_active": True}
    >>> fields = infer_fields_from_json(data)
    >>> fields["user_id"]
    'int'
    >>> fields["username"]
    'str'
    >>> fields["is_active"]
    'bool'
    """
    fields: dict[str, str] = {}
    for key, value in data.items():
        fields[key] = infer_python_type(value)
    return fields
