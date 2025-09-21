"""Factory for obtaining appropriate data structure builders."""

from aste.datastructures.base import DataStructureBuilder
from aste.datastructures.builders import AttrsBuilder
from aste.datastructures.builders import DataclassBuilder
from aste.datastructures.builders import NamedTupleBuilder
from aste.datastructures.builders import PydanticBuilder
from aste.datastructures.builders import TypedDictBuilder


class DataStructureFactory:
    """
    Factory to obtain appropriate DataStructureBuilder by type name.

    Examples
    --------
    >>> builder = DataStructureFactory.get_builder("typed_dict")
    >>> isinstance(builder, TypedDictBuilder)
    True
    >>> builder = DataStructureFactory.get_builder("dataclass")
    >>> isinstance(builder, DataclassBuilder)
    True
    """

    @staticmethod
    def get_builder(builder_type: str) -> DataStructureBuilder:
        """
        Return the builder instance corresponding to the given type.

        Parameters
        ----------
        builder_type : str
            Type identifier: "typed_dict", "dataclass", "pydantic",
            "namedtuple", or "attrs"

        Returns
        -------
        DataStructureBuilder
            Builder instance for the requested type

        Raises
        ------
        ValueError
            If builder_type is not recognized

        Examples
        --------
        >>> factory = DataStructureFactory()
        >>> builder = factory.get_builder("pydantic")
        >>> code = builder.build("User", {"id": "int"})
        >>> "BaseModel" in code
        True
        """
        mapping: dict[str, DataStructureBuilder] = {
            "typed_dict": TypedDictBuilder(),
            "dataclass": DataclassBuilder(),
            "pydantic": PydanticBuilder(),
            "namedtuple": NamedTupleBuilder(),
            "attrs": AttrsBuilder(),
        }
        try:
            return mapping[builder_type]
        except KeyError as exc:
            message = f"Unknown builder type: {builder_type}"
            raise ValueError(message) from exc
