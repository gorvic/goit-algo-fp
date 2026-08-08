import heapq

from binary_tree import build_heap_tree, draw_tree

if __name__ == "__main__":
    heap = [1, 3, 5, 7, 9, 2]
    heapq.heapify(heap)

    print(f"Heap: {heap}")

    root = build_heap_tree(heap)
    draw_tree(root, "skyblue")
