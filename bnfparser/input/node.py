"""input node module"""

from dataclasses import dataclass, field
from typing import Union, List, Dict
from enum import Enum

DEFAULT_GRAPHVIZ_ATTRS = {
    "style": "filled",
    "fillcolor": "lightgrey",
}

class Nodekind(Enum):
    """Represents a node kind
    """

    VARIABLE = "variable"
    VALUE = "value"

@dataclass
class BaseInputNode:
    """Represents an input node"""
    node_kind: str = ""
    value: str = ""
    parent: Union["InputNode", None] = None
    childrens: List["InputNode"] = field(default_factory=list)

    def __str__(self) -> str:
        ret = (self.node_kind, self.value)
        return str(ret)

@dataclass
class InputNode(BaseInputNode):
    """Representing a Graphviz node"""

    @property
    def name(self) -> str:
        """Graphviz Node name

        Returns:
            str: The node name
        """
        return str(id(self))

    @property
    def attrs(self) -> Dict[str, str]:
        """Return Graphviz attributes

        Returns:
            Dict[str, str]: Graphviz attributes
        """

        if self.node_kind == Nodekind.VARIABLE:
            return {}

        return DEFAULT_GRAPHVIZ_ATTRS
