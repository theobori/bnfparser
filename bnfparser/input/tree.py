"""input tree module"""

import graphviz

from .node import InputNode

class BaseInputTree:
    """Represents the input AST
    """

    def __init__(self):
        self.root = InputNode()
        self.current = self.root

    def reset(self):
        """Reset the tree members
        """

        self.root = InputNode()
        self.current = self.root

    def __create_node(self, node_kind: str, value: str) -> InputNode:
        return InputNode(node_kind, value, self.current)

    def add_and_forward(self, node_kind: str, value: str):
        """Call `self.add` the move the current cursor on the new added node

        Args:
            node_kind (str): The node type
            value (str): The node value
        """

        # Add the node
        node = self.add(node_kind, value)

        # Go forward on the node
        self.current = node

    def add_children(self, node: InputNode):
        """Add a children to the current node

        Args:
            node (InputNode): The children to add
        """

        self.current.childrens.append(node)

    def add(self, node_kind: str, value: str) -> InputNode:
        """Add a new node to the current node childrens

        Args:
            node_kind (str): The node type
            value (str): The node value
        
        Returns:
            InputNode: Returns the added node
        """

        node = self.__create_node(node_kind, value)

        self.add_children(node)

        return node

    def _debug(self):
        """BFS print to debug the tree
        """

        line = [self.root]

        while line:
            size = len(line)

            display = []

            for i in range(size):
                childrens = line[i].childrens

                for children in childrens:
                    display.append(children)
                    line.append(children)

            line = line[size:]

            if display:
                print(", ".join(map(str, display)))

    def back(self):
        """The current node become the parent of the current node
        """

        parent = self.current.parent

        if parent is None:
            return

        self.current = parent

class InputTree(graphviz.Graph, BaseInputTree):
    """Graphviz controller inheriting `BaseTreeInput`

    Args:
        graphviz (graphviz.Graph): graphviz.Graph
        BaseInputTree (BaseInputTree): BaseInputTree
    """

    def build_graph(self):
        """Link every node with Graphviz"""

        def dfs(node: InputNode):
            """Link every node with Graphviz

            Args:
                node (Node): Node
            """

            if node.parent is None:
                for children in node.childrens:
                    dfs(children)

                return

            # Parent
            self.node(
                node.name,
                node.value,
                **node.attrs,
            )

            # Childrens
            for children in node.childrens:
                self.node(
                    children.name,
                    children.value,
                    **children.attrs,
                )

                self.edge(node.name, children.name)

                dfs(children)

        dfs(self.root)

        return self
