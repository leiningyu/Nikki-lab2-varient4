class Node:
    def __init__(self, value, next_=None):
        self._value = value
        self._next = next_

    def __str__(self):
        if self._next is None:
            return str(self._value)
        return f"{self._value} : {self._next}"

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Node):
            return False
        return self._value == other._value and self._next == other._next

# Monoid Empty element
def empty():
    return None

# Construct a new node
def cons(value, next_):
    return Node(value, next_)

# Gets the header node value
def head(node):
    assert isinstance(node, Node), "Cannot get head of empty list"
    return node._value

# Get tail node
def tail(node):
    assert isinstance(node, Node), "Cannot get tail of empty list"
    return node._next

# Add an element to the list header (keep it immutable)
def add(lst, value):
    return cons(value, lst)

# Recursively deletes the first matching value
def remove(lst, value):
    assert lst is not None, "List cannot be None"
    def _remove_helper(node):
        if node is None:
            return None
        if head(node) == value:
            return tail(node)
        return cons(head(node), _remove_helper(tail(node)))
    return _remove_helper(lst)

# Calculate the size recursively
def size(lst):
    return 0 if lst is None else 1 + size(tail(lst))

# Recursive member checking
def is_member(lst, value):
    if lst is None:
        return False
    return head(lst) == value or is_member(tail(lst), value)

# Recursively reverse a linked list
def reverse(lst, acc=None):
    return acc if lst is None else reverse(tail(lst), cons(head(lst), acc))

# Recursively find the intersection of sets
def intersection(a, b):
    def _intersect(a, b, seen):
        if a is None:
            return empty()
        h = head(a)
        t = tail(a)
        if is_member(seen, h):
            return _intersect(t, b, seen)
        if is_member(b, h):
            return cons(h, _intersect(t, b, cons(h, seen)))
        return _intersect(t, b, seen)
    return _intersect(a, b, empty())

# Recursive conversion to Python list
def to_list(lst):
    return [] if lst is None else [head(lst)] + to_list(tail(lst))

# Recursion builds from Python lists
def from_list(pylist):
    def _build(index):
        return empty() if index >= len(pylist) else cons(
            pylist[index], _build(index+1))
    return _build(0)

# Recursively finds the element that satisfies the condition
def find(lst, predicate):
    if lst is None:
        return None
    return head(lst) if predicate(head(lst)) else find(tail(lst), predicate)

# Recursive filtering
def filter(lst, predicate):
    if lst is None:
        return empty()
    h = head(lst)
    t = tail(lst)
    return cons(h, filter(t, predicate)) if predicate(h) else filter(t, predicate)

# Recursive mapping
def map(lst, func):
    return empty() if lst is None else cons(func(head(lst)), map(tail(lst), func))

# Recursive reduction
def reduce(lst, func, initial):
    return initial if lst is None else reduce(tail(lst), func, func(initial, head(lst)))

# A functional iterator
def iterator(lst):
    current = lst
    def next():
        nonlocal current
        if current is None:
            raise StopIteration
        val = head(current)
        current = tail(current)
        return val
    return next

# Monoid Connection operation
def concat(a, b):
    def _concat(a, b):
        return b if a is None else cons(head(a), _concat(tail(a), b))
    return _concat(a, b)

# Recursive equality checking
def equals(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return head(a) == head(b) and equals(tail(a), tail(b))

# String serialization
def to_string(lst):
    return str(lst) if lst else "Empty"
