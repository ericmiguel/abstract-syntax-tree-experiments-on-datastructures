"""Concrete implementations of data structure builders."""

import ast

from aste.datastructures.base import DataStructureBuilder


class TypedDictBuilder(DataStructureBuilder):
    """
    Builder for Python TypedDict structures using AST.

    Examples
    --------
    >>> builder = TypedDictBuilder()
    >>> code = builder.build("User", {"id": "int", "name": "str"})
    >>> "from typing import TypedDict" in code
    True
    >>> "class User(TypedDict):" in code
    True
    """

    def _build_imports(self, class_name: str, fields: dict[str, str]) -> list[ast.stmt]:
        return [
            ast.ImportFrom(
                module="typing", names=[ast.alias(name="TypedDict")], level=0
            )
        ]

    def _build_body_nodes(
        self, class_name: str, fields: dict[str, str]
    ) -> list[ast.stmt]:
        nodes: list[ast.stmt] = []
        for name, typ in fields.items():
            nodes.append(
                ast.AnnAssign(
                    target=ast.Name(id=name, ctx=ast.Store()),
                    annotation=ast.Name(id=typ, ctx=ast.Load()),
                    simple=1,
                )
            )
        if not nodes:
            nodes.append(ast.Pass())
        return nodes

    def _build_bases(self, class_name: str, fields: dict[str, str]) -> list[ast.expr]:
        return [ast.Name(id="TypedDict", ctx=ast.Load())]


class DataclassBuilder(DataStructureBuilder):
    """
    Builder for Python dataclass structures using AST.

    Examples
    --------
    >>> builder = DataclassBuilder()
    >>> code = builder.build("User", {"id": "int", "name": "str"})
    >>> "from dataclasses import dataclass" in code
    True
    >>> "@dataclass" in code
    True
    """

    def _build_imports(self, class_name: str, fields: dict[str, str]) -> list[ast.stmt]:
        return [
            ast.ImportFrom(
                module="dataclasses",
                names=[ast.alias(name="dataclass")],
                level=0,
            )
        ]

    def _build_body_nodes(
        self, class_name: str, fields: dict[str, str]
    ) -> list[ast.stmt]:
        nodes: list[ast.stmt] = []
        for name, typ in fields.items():
            nodes.append(
                ast.AnnAssign(
                    target=ast.Name(id=name, ctx=ast.Store()),
                    annotation=ast.Name(id=typ, ctx=ast.Load()),
                    simple=1,
                )
            )
        if not nodes:
            nodes.append(ast.Pass())
        return nodes

    def _build_bases(self, class_name: str, fields: dict[str, str]) -> list[ast.expr]:
        return []

    def _build_decorators(
        self, class_name: str, fields: dict[str, str]
    ) -> list[ast.expr]:
        return [ast.Name(id="dataclass", ctx=ast.Load())]


class PydanticBuilder(DataStructureBuilder):
    """
    Builder for Pydantic BaseModel structures using AST.

    Examples
    --------
    >>> builder = PydanticBuilder()
    >>> code = builder.build("User", {"id": "int", "name": "str"})
    >>> "from pydantic import BaseModel" in code
    True
    >>> "class User(BaseModel):" in code
    True
    """

    def _build_imports(self, class_name: str, fields: dict[str, str]) -> list[ast.stmt]:
        return [
            ast.ImportFrom(
                module="pydantic", names=[ast.alias(name="BaseModel")], level=0
            )
        ]

    def _build_body_nodes(
        self, class_name: str, fields: dict[str, str]
    ) -> list[ast.stmt]:
        nodes: list[ast.stmt] = []
        for name, typ in fields.items():
            nodes.append(
                ast.AnnAssign(
                    target=ast.Name(id=name, ctx=ast.Store()),
                    annotation=ast.Name(id=typ, ctx=ast.Load()),
                    simple=1,
                )
            )
        if not nodes:
            nodes.append(ast.Pass())
        return nodes

    def _build_bases(self, class_name: str, fields: dict[str, str]) -> list[ast.expr]:
        return [ast.Name(id="BaseModel", ctx=ast.Load())]


class NamedTupleBuilder(DataStructureBuilder):
    """
    Builder for NamedTuple structures using AST.

    Examples
    --------
    >>> builder = NamedTupleBuilder()
    >>> code = builder.build("User", {"id": "int", "name": "str"})
    >>> "from typing import NamedTuple" in code
    True
    >>> "class User(NamedTuple):" in code
    True
    """

    def _build_imports(self, class_name: str, fields: dict[str, str]) -> list[ast.stmt]:
        return [
            ast.ImportFrom(
                module="typing", names=[ast.alias(name="NamedTuple")], level=0
            )
        ]

    def _build_body_nodes(
        self, class_name: str, fields: dict[str, str]
    ) -> list[ast.stmt]:
        nodes: list[ast.stmt] = []
        for name, typ in fields.items():
            nodes.append(
                ast.AnnAssign(
                    target=ast.Name(id=name, ctx=ast.Store()),
                    annotation=ast.Name(id=typ, ctx=ast.Load()),
                    simple=1,
                )
            )
        if not nodes:
            nodes.append(ast.Pass())
        return nodes

    def _build_bases(self, class_name: str, fields: dict[str, str]) -> list[ast.expr]:
        return [ast.Name(id="NamedTuple", ctx=ast.Load())]


class AttrsBuilder(DataStructureBuilder):
    """
    Builder for attrs classes using AST with attr.define decorator.

    Examples
    --------
    >>> builder = AttrsBuilder()
    >>> code = builder.build("User", {"id": "int", "name": "str"})
    >>> "from attr import define" in code
    True
    >>> "@define" in code
    True
    """

    def _build_imports(self, class_name: str, fields: dict[str, str]) -> list[ast.stmt]:
        return [
            ast.ImportFrom(module="attr", names=[ast.alias(name="define")], level=0)
        ]

    def _build_body_nodes(
        self, class_name: str, fields: dict[str, str]
    ) -> list[ast.stmt]:
        nodes: list[ast.stmt] = []
        for name, typ in fields.items():
            nodes.append(
                ast.AnnAssign(
                    target=ast.Name(id=name, ctx=ast.Store()),
                    annotation=ast.Name(id=typ, ctx=ast.Load()),
                    simple=1,
                )
            )
        if not nodes:
            nodes.append(ast.Pass())
        return nodes

    def _build_bases(self, class_name: str, fields: dict[str, str]) -> list[ast.expr]:
        return []

    def _build_decorators(
        self, class_name: str, fields: dict[str, str]
    ) -> list[ast.expr]:
        return [ast.Name(id="define", ctx=ast.Load())]
