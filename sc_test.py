import hypothesis.strategies as st
import pytest
from hypothesis import given
from sc import (
    ImmutableHashTable, cons, empty, remove, reverse,
    size, to_list, from_list, is_member, concat,
    intersection, filter, map, ht_reduce, equals, to_string,
    iterator
)


# ------------------- Unit Tests -------------------
def test_size():
    ht = empty()
    assert size(ht) == 0
    ht = cons("a", ht)
    assert size(ht) == 1
    ht = cons("b", ht)
    assert size(ht) == 2


def test_cons():
    ht = cons("a", empty())
    assert "a" in to_list(ht)
    ht = cons("b", ht)
    assert sorted(to_list(ht)) == ["a", "b"]


def test_remove():
    ht = from_list([1, 2, 3])
    ht = remove(ht, 2)
    assert sorted(to_list(ht)) == [1, 3]


def test_is_member():
    ht = from_list([1, 2, 3])
    assert is_member(ht, 2) is True
    assert is_member(ht, 4) is False


def test_reverse():
    ht = from_list([1, 2, 3])
    reversed_ht = reverse(ht)
    assert equals(reverse(reversed_ht), ht)


def test_concat():
    ht1 = from_list([1, 2])
    ht2 = from_list([3, 4])
    combined = concat(ht1, ht2)
    assert sorted(to_list(combined)) == [1, 2, 3, 4]


def test_intersection():
    empty_ht = empty()
    ht1 = from_list([1, 2, 3])
    assert to_list(intersection(ht1, empty_ht)) == []
    assert to_list(intersection(empty_ht, ht1)) == []
    
    ht2 = from_list([1, 2, 3])
    ht3 = from_list([2, 3, 4])
    inter_partial = intersection(ht2, ht3)
    assert sorted(to_list(inter_partial)) == [2, 3]


def test_to_list():
    lst = [3, 1, 4, 2]
    ht = from_list(lst)
    assert sorted(to_list(ht)) == sorted(lst)


def test_from_list():
    lst = [5, 2, 8, 1]
    ht = from_list(lst)
    assert sorted(to_list(ht)) == sorted(lst)


def test_filter():
    ht = from_list([1, 2, 3, 4])
    filtered = filter(ht, lambda x: x % 2 == 0)
    assert sorted(to_list(filtered)) == [2, 4]


def test_map():
    ht = from_list([1, 2, 3])
    mapped = map(ht, lambda x: x * 2)
    assert sorted(to_list(mapped)) == [2, 4, 6]


def test_reduce():
    ht = from_list([1, 2, 3, 4])
    result = ht_reduce(ht, lambda acc, x: acc + x, 0)
    assert result == 10


def test_equals():
    ht1 = from_list([1, 2, 3])
    ht2 = from_list([1, 2, 3])
    ht3 = from_list([1, 2])
    assert equals(ht1, ht2) is True
    assert equals(ht1, ht3) is False


def test_to_string():
    assert to_string(empty()) == "Empty"
    ht = cons("b", cons("a", empty()))
    assert "a" in to_string(ht) and "b" in to_string(ht)


def test_iterator():
    lst = [1, 2, 3]
    ht = from_list(lst)
    collected = []
    for item in iterator(ht):
        collected.append(item)
    assert sorted(collected) == sorted(lst)


# ------------------- API Tests -------------------
def test_api():
    empty = ImmutableHashTable()
    assert to_string(empty) == "Empty"
    table_with_none = cons(None, empty)
    assert "None" in to_string(table_with_none)

    ht1 = cons(1, cons(None, empty))
    ht2 = cons(None, cons(1, empty))
    assert "1" in to_string(ht1) and "None" in to_string(ht1)
    assert equals(ht1, ht2)
    
    # size
    assert size(empty) == 0
    assert size(ht1) == 2
    
    # remove
    removed_none = remove(ht1, None)
    assert to_list(removed_none) == [1]
    
    removed_one = remove(ht1, 1)
    assert to_list(removed_one) == [None]
    
    # member
    assert not is_member(empty, None)
    assert is_member(ht1, None)
    assert is_member(ht1, 1)
    assert not is_member(ht1, 2)
    
    # intersection
    inter = intersection(ht1, ht2)
    assert to_list(inter) == [1, None] or to_list(inter) == [None, 1]
    
    # to_from_list
    to_list(ht1) == [1, None] or to_list(ht1) == [None, 1]
    assert equals(ht1, from_list([1, None]))
    assert equals(ht1, from_list([1, None, 1]))
    
    # concat
    combined = concat(ht1, ht2)
    assert equals(combined, from_list([None, 1, 1, None]))
    
    # iterator
    collected = []
    for item in iterator(ht1):
        collected.append(item)
    assert collected == [1, None] or collected == [None, 1]
    
    # filter
    numbers = from_list([1, 2, 3, 4])
    even = filter(numbers, lambda x: x % 2 == 0)
    assert sorted(to_list(even)) == [2, 4]
    
    # map
    doubled = map(numbers, lambda x: x * 2)
    assert sorted(to_list(doubled)) == [2, 4, 6, 8]
    
    # reduce
    sum_result = ht_reduce(numbers, lambda acc, x: acc + x, 0)
    assert sum_result == 10
    
    # empty
    assert ht_reduce(empty, lambda acc, x: acc + x, 0) == 0


# ------------------- Property-Based Tests -------------------
@given(st.lists(st.integers(), unique=True))
def test_from_list_to_list_equality(a):
    assert sorted(to_list(from_list(a))) == sorted(a)


@given(st.lists(st.integers(), unique=True))
def test_monoid_identity(b):
    a = from_list(b)
    assert equals(concat(empty(), a), a)
    assert equals(concat(a, empty()), a)


@given(st.lists(st.integers(), unique=True))
def test_size_consistency(a):
    assert size(from_list(a)) == len(a)


if __name__ == "__main__":
    pytest.main()
