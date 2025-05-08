from functools import reduce
from typing import Callable, Any, Iterator


class ImmutableNode:
    def __init__(self, value, next_=None):
        self._value = value
        self._next = next_

    def __str__(self):
        return f"{self._value} -> {self._next}" \
            if self._next \
            else str(self._value)

    def __eq__(self, other):
        return isinstance(other, ImmutableNode) and \
            self._value == other._value and \
            self._next == other._next


class ImmutableHashTable:
    def __init__(self, buckets=None, size=10):
        self._size = size
        self._buckets = buckets if buckets is not None else tuple(
            None for _ in range(size))

    def _hash(self, value) -> int:
        return hash(value) % self._size

    def is_empty(self) -> bool:
        return all(bucket is None for bucket in self._buckets)

    def _get_bucket(self, index: int) -> ImmutableNode:
        return self._buckets[index]

    def _with_updated_bucket(
            self, index: int, new_head) -> 'ImmutableHashTable':
        new_buckets = list(self._buckets)
        new_buckets[index] = new_head
        return ImmutableHashTable(tuple(new_buckets), self._size)


def ht_empty() -> ImmutableHashTable:
    return ImmutableHashTable()


def ht_cons(value, ht: ImmutableHashTable) -> ImmutableHashTable:
    index = ht._hash(value)
    current = ht._get_bucket(index)

    # Check repetition
    def contains(node):
        while node is not None:
            if node._value == value:
                return True
            node = node._next
        return False

    if contains(current):
        return ht

    # Insert new node
    return ht._with_updated_bucket(
        index, ImmutableNode(value, current))


def ht_head(node: ImmutableNode):
    if node is None:
        raise ValueError("Empty node")
    return node._value


def ht_tail(node: ImmutableNode) -> ImmutableNode:
    if node is None:
        raise ValueError("Empty node")
    return node._next


def ht_remove(ht: ImmutableHashTable, value) -> ImmutableHashTable:
    index = ht._hash(value)
    current = ht._get_bucket(index)

    def _remove(node):
        if node is None:
            return None
        if node._value == value:
            return node._next
        return ImmutableNode(node._value, _remove(node._next))

    return ht._with_updated_bucket(index, _remove(current))


def ht_size(ht: ImmutableHashTable) -> int:
    if ht.is_empty():
        return 0

    def count(node):
        return 0 if node is None else 1 + count(node._next)
    return sum(count(bucket) for bucket in ht._buckets)


def ht_member(ht: ImmutableHashTable, value) -> bool:
    index = ht._hash(value)

    def check(node):
        return node is not None and (
            node._value == value or check(node._next))
    return check(ht._get_bucket(index))


def ht_reverse(ht: ImmutableHashTable) -> ImmutableHashTable:
    def reverse_bucket(node, acc=None):
        return acc if node is None else reverse_bucket(
            node._next, ImmutableNode(node._value, acc))

    new_buckets = []
    for bucket in ht._buckets:
        new_buckets.append(reverse_bucket(bucket))
    return ImmutableHashTable(tuple(new_buckets), ht._size)


def ht_intersection(
        a: ImmutableHashTable,
        b: ImmutableHashTable
        ) -> ImmutableHashTable:
    def traverse(node, acc):
        if node is None:
            return acc
        if ht_member(b, node._value):
            return traverse(node._next, ht_cons(node._value, acc))
        return traverse(node._next, acc)

    result = ht_empty()
    for bucket in a._buckets:
        result = traverse(bucket, result)
    return result


def to_list(ht: ImmutableHashTable) -> list:
    # convert to list
    def collect(node, acc):
        return acc if node is None else collect(
            node._next, [node._value] + acc)
    return [item for bucket in ht._buckets for item in collect(bucket, [])]


def from_list(lst: list) -> ImmutableHashTable:
    # convert to hashtable
    return reduce(lambda acc, x: ht_cons(x, acc), lst, ht_empty())


def ht_find(ht: ImmutableHashTable, predicate: Callable[[Any], bool]):
    # find the element that satisfies the condition
    for bucket in ht._buckets:
        current = bucket
        while current:
            if predicate(current._value):
                return current._value
            current = current._next
    return None


def ht_filter(
        ht: ImmutableHashTable,
        predicate: Callable[[Any], bool]
        ) -> ImmutableHashTable:
    def filter_bucket(node):
        if node is None:
            return None
        return (
            ImmutableNode(node._value, filter_bucket(node._next))
            if predicate(node._value)
            else filter_bucket(node._next)
        )

    new_buckets = []
    for bucket in ht._buckets:
        new_buckets.append(filter_bucket(bucket))
    return ImmutableHashTable(tuple(new_buckets), ht._size)


def ht_map(
    ht: ImmutableHashTable,
    func: Callable[[Any], Any]
    ) -> ImmutableHashTable:
    new_ht = ImmutableHashTable(size=ht._size)
    for value in ht_iterator(ht):
        new_ht = ht_cons(func(value), new_ht)
    return new_ht



def ht_reduce(
        ht: ImmutableHashTable,
        func: Callable[[Any, Any], Any],
        initial
        ) -> Any:
    acc = initial
    for bucket in ht._buckets:
        current = bucket
        while current:
            acc = func(acc, current._value)
            current = current._next
    return acc


def ht_concat(
        a: ImmutableHashTable,
        b: ImmutableHashTable
        ) -> ImmutableHashTable:

    def contains(node, value):
        # Check whether the value exists in the linked list
        if node is None:
            return False
        return node._value == value or contains(node._next, value)

    def merge_bucket(bucket_a, bucket_b):
        # Merge two bucket lists and de-duplicate
        if bucket_a is None:
            return bucket_b

        # Decide whether to add the current node after
        # processing the subsequent nodes
        merged_next = merge_bucket(bucket_a._next, bucket_b)

        if contains(merged_next, bucket_a._value):
            return merged_next
        return ImmutableNode(bucket_a._value, merged_next)

    new_buckets = []
    for ba, bb in zip(a._buckets, b._buckets):
        # Bidirectional merge: a->b and b->a fetch union
        temp = merge_bucket(ba, bb)
        temp = merge_bucket(bb, temp)
        new_buckets.append(temp)
    return ImmutableHashTable(tuple(new_buckets), a._size)


def ht_equals(a: ImmutableHashTable, b: ImmutableHashTable) -> bool:
    if a.is_empty() and b.is_empty():
        return True

    for i in ht_iterator(a):
        if not ht_member(b, i):
            return False

    for i in ht_iterator(b):
        if not ht_member(a, i):
            return False
    return True

def ht_iterator(ht: ImmutableHashTable) -> Iterator:
    items = to_list(ht)
    while items:
        yield items.pop(0)


def to_string(ht: ImmutableHashTable) -> str:
    if ht.is_empty():
        return "Empty"
    return "\n".join(
        f"Bucket {i}: {bucket}" if bucket else f"Bucket {i}: Empty"
        for i, bucket in enumerate(ht._buckets)
    )
