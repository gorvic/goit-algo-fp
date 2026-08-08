import heapq
import uuid

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    """Represent a node of a binary tree."""

    def __init__(self, key: int, color: str = "skyblue") -> None:
        self.left: Node | None = None
        self.right: Node | None = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(
        graph: nx.DiGraph, node: Node | None, pos: dict,
        x: float = .0, y: float = .0, layer: int = 1,
) -> nx.DiGraph:
    """Add tree nodes and edges to the graph."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)

        if node.left:
            graph.add_edge(node.id, node.left.id)
            left = x - 1 / 2 ** layer
            pos[node.left.id] = (left, y - 1)
            add_edges(graph, node.left, pos, left, y - 1, layer + 1)

        if node.right:
            graph.add_edge(node.id, node.right.id)
            right = x + 1 / 2 ** layer
            pos[node.right.id] = (right, y - 1)
            add_edges(graph, node.right, pos, right, y - 1, layer + 1)

    return graph


def draw_tree(tree_root: Node) -> None:
    """Visualize a binary tree."""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {node: data["label"] for node, data in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()


def build_heap_tree(heap: list[int], index: int = 0) -> Node | None:
    """Build a binary tree from a heap."""
    if index >= len(heap):
        return None

    node = Node(heap[index])
    node.left = build_heap_tree(heap, 2 * index + 1)
    node.right = build_heap_tree(heap, 2 * index + 2)

    return node


if __name__ == "__main__":
    heap = [1, 3, 5, 7, 9, 2]
    heapq.heapify(heap)

    print(f"Heap: {heap}")

    heap_tree_root = build_heap_tree(heap)
    draw_tree(heap_tree_root)
