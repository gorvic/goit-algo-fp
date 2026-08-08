from collections.abc import Iterable, Iterator


class Node:
    """Represent a node of a singly linked list."""

    def __init__(self, data: int) -> None:
        self.data = data
        self.next: Node | None = None


class LinkedList:
    """Represent a singly linked list."""

    def __init__(self, values: Iterable[int] = ()) -> None:
        self._head: Node | None = None
        self._tail: Node | None = None
        self._is_sorted = True

        for value in values:
            self.append(value)

    def prepend(self, value: int) -> None:
        """Prepend a value to the beginning of the list."""
        node = Node(value)

        if self._head is None:
            self._head = self._tail = node
            return

        if self._is_sorted and value > self._head.data:
            self._is_sorted = False

        node.next = self._head
        self._head = node

    def append(self, value: int) -> None:
        """Append a value to the end of the list."""
        node = Node(value)

        if self._head is None:
            self._head = self._tail = node
            return

        if self._is_sorted and self._tail.data > value:
            self._is_sorted = False

        self._tail.next = node
        self._tail = node

    def remove(self, value: int) -> bool:
        """Remove the first occurrence of a value."""
        previous = None
        current = self._head

        while current is not None:
            if self._is_sorted and current.data > value:
                break

            if current.data == value:
                if previous is None:
                    self._head = current.next
                else:
                    previous.next = current.next

                if current is self._tail:
                    self._tail = previous

                return True

            previous = current
            current = current.next

        return False

    def reverse(self) -> None:
        """Reverse the list by changing links between nodes."""
        if self._head is None or self._head.next is None:
            return

        previous = None
        current = self._head
        self._tail = self._head

        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self._head = previous
        self._is_sorted = False

    def sort(self) -> None:
        """Sort the list using merge sort."""
        if self._is_sorted:
            return

        self._head = self._merge_sort(self._head)
        self._refresh_tail()
        self._is_sorted = True

    def merge_and_sort(self, *lists: "LinkedList") -> None:
        """Append linked lists and sort the result."""
        for linked_list in lists:
            for value in linked_list:
                self.append(value)

        self.sort()

    @staticmethod
    def merge_sorted_lists(first: "LinkedList", second: "LinkedList") -> "LinkedList":
        """Merge two sorted linked lists into a new sorted list."""
        result = LinkedList()
        left = first._head
        right = second._head

        while left is not None and right is not None:
            if left.data <= right.data:
                result.append(left.data)
                left = left.next
            else:
                result.append(right.data)
                right = right.next

        current = left or right

        while current is not None:
            result.append(current.data)
            current = current.next

        return result

    def __iter__(self) -> Iterator[int]:
        current = self._head

        while current is not None:
            yield current.data
            current = current.next

    def __str__(self) -> str:
        return " -> ".join(map(str, self)) or "None"

    @classmethod
    def _merge_sort(cls, head: Node | None) -> Node | None:
        if head is None or head.next is None:
            return head

        middle = cls._get_middle(head)
        right = middle.next
        middle.next = None

        return cls._sorted_merge(
            cls._merge_sort(head),
            cls._merge_sort(right),
        )

    @staticmethod
    def _get_middle(head: Node) -> Node:
        slow = head
        fast = head.next

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

        return slow

    @staticmethod
    def _sorted_merge(left: Node | None, right: Node | None) -> Node | None:
        dummy = tail = Node(0)

        while left is not None and right is not None:
            if left.data <= right.data:
                tail.next = left
                left = left.next
            else:
                tail.next = right
                right = right.next

            tail = tail.next

        tail.next = left or right

        return dummy.next

    def _refresh_tail(self) -> None:
        self._tail = self._head

        while self._tail is not None and self._tail.next is not None:
            self._tail = self._tail.next


if __name__ == "__main__":
    first_list = LinkedList()

    first_list.prepend(5)
    first_list.prepend(10)
    first_list.prepend(15)
    first_list.append(20)
    first_list.append(25)
    print("First linked list:")
    print(first_list)

    first_list.reverse()
    print("First linked list after reversing:")
    print(first_list)

    first_list.sort()
    print("First linked list after sorting:")
    print(first_list)

    second_list = LinkedList()
    second_list.prepend(59)
    second_list.prepend(20)
    second_list.prepend(35)
    print("Second linked list:")
    print(second_list)

    second_list.sort()
    print("Second linked list after sorting:")
    print(second_list)

    first_list.merge_and_sort(second_list)
    print("First linked list merged with the second and sorted:")
    print(first_list)

    print()

    first_list = LinkedList([15, 10, 5, 20, 25])
    second_list = LinkedList([35, 20, 59])

    first_list.sort()
    second_list.sort()

    merged_list = LinkedList.merge_sorted_lists(first_list, second_list)
    print("Merge of two sorted linked lists:")
    print(merged_list)
