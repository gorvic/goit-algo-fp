import colorsys
import matplotlib.pyplot as plt
import networkx as nx
import uuid

from collections import deque


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
        graph.add_node(node.id, label=node.val)

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


def draw_tree(tree_root: Node, colors: dict[str, str] | str = "skyblue", title: str | None = None) -> None:
    """Visualize a binary tree."""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [
        colors if isinstance(colors, str) else colors.get(node, "skyblue")
        for node in tree.nodes
    ]
    labels = {node: data["label"] for node, data in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))

    if title:
        plt.title(title)

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


def dfs_visualize(root: Node, total_steps: int) -> dict[str, str]:
    """Return node colors in depth-first traversal order."""
    colors = {}
    stack = [root]

    for step in range(total_steps):
        node = stack.pop()
        colors[node.id] = generate_color(step, total_steps)

        if node.right:
            stack.append(node.right)

        if node.left:
            stack.append(node.left)

    return colors


def bfs_visualize(root: Node, total_steps: int) -> dict[str, str]:
    """Return node colors in breadth-first traversal order."""
    colors = {}
    queue = deque([root])

    for step in range(total_steps):
        node = queue.popleft()
        colors[node.id] = generate_color(step, total_steps)

        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)

    return colors


def generate_color(step: int, total_steps: int) -> str:
    """Generate a smooth color gradient according to traversal order."""
    factor = step / max(total_steps - 1, 1)
    hue = 240 * (1 - factor) / 360

    red, green, blue = colorsys.hsv_to_rgb(hue, 0.9, 0.9)

    return (
        f"#{round(red * 255):02X}"
        f"{round(green * 255):02X}"
        f"{round(blue * 255):02X}"
    )
