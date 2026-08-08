import heapq

from binary_tree import build_heap_tree, draw_tree, bfs_visualize, dfs_visualize

if __name__ == "__main__":
    heap = [1, 3, 5, 7, 9, 2, 4, 34, 2, 1, 2]
    heapq.heapify(heap)

    root = build_heap_tree(heap)
    total_steps = len(heap)

    print(f"Heap: {heap}")

    dfs_colors = dfs_visualize(root, total_steps)
    draw_tree(root, dfs_colors, title="DFS traversal")

    bfs_colors = bfs_visualize(root, total_steps)
    draw_tree(root, bfs_colors, title="BFS traversal")
