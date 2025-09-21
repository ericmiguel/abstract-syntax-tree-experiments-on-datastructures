"""Abstract base class for data structure builders."""

from abc import ABC
from abc import abstractmethod
import ast


class DataStructureBuilder(ABC):
    """
    Abstract base class for data structure builders.

    Implementations should generate code for different data structures
    (e.g., TypedDict, dataclass, Pydantic model).

    Examples
    --------
    >>> class CustomBuilder(DataStructureBuilder):
    ...     def _build_imports(self, class_name, fields):
    ...         return []
    ...
    ...     def _build_body_nodes(self, class_name, fields):
    ...         return [ast.Pass()]
    ...
    ...     def _build_bases(self, class_name, fields):
    ...         return []
    >>> builder = CustomBuilder()
    >>> code = builder.build("MyClass", {"field": "str"})
    """

    @abstractmethod
    def _build_imports(self, class_name: str, fields: dict[str, str]) -> list[ast.stmt]:
        """Return list of AST import nodes."""
        ...

    @abstractmethod
    def _build_body_nodes(
        self, class_name: str, fields: dict[str, str]
    ) -> list[ast.stmt]:
        """Return list of AST nodes for class body."""
        ...

    @abstractmethod
    def _build_bases(self, class_name: str, fields: dict[str, str]) -> list[ast.expr]:
        """Return list of AST nodes for class bases."""
        ...

    def _build_decorators(
        self, class_name: str, fields: dict[str, str]
    ) -> list[ast.expr]:
        """Return list of AST nodes for class decorators (optional)."""
        return []

    def build(self, class_name: str, fields: dict[str, str]) -> str:
        """
        Assemble import nodes, class definition, and module.

        Parameters
        ----------
        class_name : str
            Name of the class to generate
        fields : dict[str, str]
            Mapping of field names to type names

        Returns
        -------
        str
            Generated Python code as string

        Examples
        --------
        >>> builder = TypedDictBuilder()
        >>> code = builder.build("User", {"id": "int", "name": "str"})
        >>> "class User(TypedDict):" in code
        True
        """
        import_nodes = self._build_imports(class_name, fields)
        body_nodes = self._build_body_nodes(class_name, fields)
        bases = self._build_bases(class_name, fields)
        decorators = self._build_decorators(class_name, fields)
        class_node = ast.ClassDef(
            name=class_name,
            bases=bases,
            keywords=[],
            body=body_nodes,
            decorator_list=decorators,
            type_params=[],
        )
        module_node = ast.Module(body=[*import_nodes, class_node], type_ignores=[])
        ast.fix_missing_locations(module_node)
        return ast.unparse(module_node)
