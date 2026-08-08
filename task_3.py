import heapq
import matplotlib.pyplot as plt
import networkx as nx

from random import randint


def dijkstra(graph: nx.Graph, start: str) -> dict[str, float]:
    """Return shortest distances from the start vertex."""
    distances = {vertex: float("inf") for vertex in graph}
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        distance, vertex = heapq.heappop(heap)

        if distance > distances[vertex]:
            continue

        for neighbor, edge in graph[vertex].items():
            new_distance = distance + edge["weight"]

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(heap, (new_distance, neighbor))

    return distances


def create_graph(
        start: str = "A",
        size: int = 6,
) -> tuple[nx.Graph, dict[str, float], str]:
    """Create a connected weighted graph and calculate the shortest distances."""
    graph = nx.Graph()
    nodes = [chr(ord(start) + i) for i in range(size)]

    for step in (1, 2):
        for i in range(size - step):
            graph.add_edge(
                nodes[i],
                nodes[i + step],
                weight=randint(1, 5),
            )

    distances = dijkstra(graph, start)

    return graph, distances, start


def draw_graph(graph: nx.Graph):
    """Draw a connected weighted graph."""
    pos = nx.spring_layout(graph, seed=42)

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=700,
        font_size=12,
    )

    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=nx.get_edge_attributes(graph, "weight"),
    )

    plt.axis("off")
    plt.show()


def print_distances(start: str, distances: dict[str, float]) -> None:
    """Print the shortest paths from start vertex to all other vertices."""
    print(f"Shortest paths from {start}:")
    for vertex, distance in distances.items():
        print(f"{start} -> {vertex}: {distance}")


if __name__ == "__main__":
    graph, distances, start = create_graph()
    print_distances(start, distances)
    draw_graph(graph)
