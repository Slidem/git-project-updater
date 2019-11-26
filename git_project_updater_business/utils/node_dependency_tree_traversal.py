from enum import Enum, auto
from abc import ABC, abstractmethod
from git_project_updater_business.models.project_dependency_tree_node import ProjectDependencyTreeNode


# traversal strategy factory

def createDependencyTreeNodeTraversalStrategy(traversal_type: TraversalStrategyType, traversal_node_observer: NodeTraversalObserver) -> ProjectDependencyTreeNodeTraversalStrategy:
    if traversal_type == TraversalStrategyType.BFS:
        return BFSTraversalStrategy(traversal_node_observer)
    if traversal_type == TraversalStrategyType.DFS:
        return DFSTraversalStrategy(traversal_node_observer)
    raise ValueError("No valid traversal strategy type passed")


# strategies.....
class TraversalStrategyType(Enum):
    DFS = auto()
    BFS = auto()


class DFSTraversalStrategy(ProjectDependencyTreeNodeTraversalStrategy):

    def __init__(self, node_traversal_observer):
        super().__init__(node_traversal_observer)

    def traverse(self, root):
        self.__traverse_helper(root, TraversalSate(1, None, root))

    def __traverse_helper(self, node, traversal_state):
        if not node:
            return

        self.node_traversal_observer.node_visited(traversal_state)

        for child in node.children:
            self.__traverse_helper(child, TraversalSate(
                level=traversal_state.level + 1,
                parent=node,
                node=child)
            )


class BFSTraversalStrategy(ProjectDependencyTreeNodeTraversalStrategy):

    def __init__(self, node_traversal_observer):
        super().__init__(node_traversal_observer)

    def traverse(self, root):
        stack = []
        stack.append(TraversalSate(1, None, root))
        while stack:
            node_state = stack.pop()
            self.node_traversal_observer.node_visited(node_state)
            for child in node_state.node.children:
                stack.append(TraversalSate(
                    node_state.level+1, node_state, child))


class ProjectDependencyTreeNodeTraversalStrategy(ABC):

    def __init__(self, node_traversal_observer: NodeTraversalObserver):
        if not node_traversal_observer:
            raise ValueError("Node traversal observr is mandatory")
        self.node_traversal_observer = node_traversal_observer

    @abstractmethod
    def traverse(self, root: ProjectDependencyTreeNode):
        pass


class NodeTraversalObserver(ABC):

    @abstractmethod
    def node_visited(self, traversal_state: TraversalSate):
        pass


class TraversalSate:
    def __init__(self, level, parent_node: ProjectDependencyTreeNode, node: ProjectDependencyTreeNode):
        self.level = level
        self.parent_node = parent_node
        self.node = node
