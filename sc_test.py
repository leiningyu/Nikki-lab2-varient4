import hypothesis.strategies as st
import pytest
from hypothesis import given
from sc import (
    ImmutableHashTable, ht_cons, ht_empty, ht_remove, ht_reverse,
    ht_size, to_list, from_list, ht_member, ht_concat,
    ht_intersection, ht_filter, ht_map, ht_reduce, ht_equals, to_string,
    ht_iterator
)


# ------------------- Unit Tests -------------------
def test_size():
    ht = ht_empty()
    assert ht_size(ht) == 0
    ht = ht_cons("a", ht)
    assert ht_size(ht) == 1
    ht = ht_cons("b", ht)
    assert ht_size(ht) == 2


def test_cons():
    ht = ht_cons("a", ht_empty())
    assert "a" in to_list(ht)
    ht = ht_cons("b", ht)
    assert sorted(to_list(ht)) == ["a", "b"]


def test_remove():
    ht = from_list([1, 2, 3])
    ht = ht_remove(ht, 2)
    assert sorted(to_list(ht)) == [1, 3]


def test_is_member():
    ht = from_list([1, 2, 3])
    assert ht_member(ht, 2) is True
    assert ht_member(ht, 4) is False


def test_reverse():
    ht = from_list([1, 2, 3])
    reversed_ht = ht_reverse(ht)
    assert ht_equals(ht_reverse(reversed_ht), ht)


def test_concat():
    ht1 = from_list([1, 2])
    ht2 = from_list([3, 4])
    combined = ht_concat(ht1, ht2)
    assert sorted(to_list(combined)) == [1, 2, 3, 4]


def test_intersection():
    empty_ht = ht_empty()
    ht1 = from_list([1, 2, 3])
    assert to_list(ht_intersection(ht1, empty_ht)) == []
    assert to_list(ht_intersection(empty_ht, ht1)) == []

    ht2 = from_list([1, 2, 3])
    ht3 = from_list([2, 3, 4])
    inter_partial = ht_intersection(ht2, ht3)
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
    filtered = ht_filter(ht, lambda x: x % 2 == 0)
    assert sorted(to_list(filtered)) == [2, 4]


def test_map():
    ht = from_list([1, 2, 3])
    mapped = ht_map(ht, lambda x: x * 2)
    assert sorted(to_list(mapped)) == [2, 4, 6]


def test_reduce():
    ht = from_list([1, 2, 3, 4])
    result = ht_reduce(ht, lambda acc, x: acc + x, 0)
    assert result == 10


def test_equals():
    ht1 = from_list([1, 2, 3])
    ht2 = from_list([1, 3, 2])
    ht3 = from_list([1, 2])
    assert ht_equals(ht1, ht2) is True
    assert ht_equals(ht1, ht3) is False


def test_to_string():
    assert to_string(ht_empty()) == "Empty"
    ht = ht_cons("b", ht_cons("a", ht_empty()))
    assert "a" in to_string(ht) and "b" in to_string(ht)


def test_iterator():
    lst = [1, 2, 3]
    ht = from_list(lst)
    collected = []
    for item in ht_iterator(ht):
        collected.append(item)
    assert sorted(collected) == sorted(lst)


# ------------------- API Tests -------------------
def test_api():
    empty = ImmutableHashTable()
    assert to_string(empty) == "Empty"
    table_with_none = ht_cons(None, empty)
    assert "None" in to_string(table_with_none)

    ht1 = ht_cons(1, ht_cons(None, empty))
    ht2 = ht_cons(None, ht_cons(1, empty))
    assert "1" in to_string(ht1) and "None" in to_string(ht1)
    assert ht_equals(ht1, ht2)

    # size
    assert ht_size(empty) == 0
    assert ht_size(ht1) == 2

    # remove
    removed_none = ht_remove(ht1, None)
    assert to_list(removed_none) == [1]

    removed_one = ht_remove(ht1, 1)
    assert to_list(removed_one) == [None]

    # member
    assert not ht_member(empty, None)
    assert ht_member(ht1, None)
    assert ht_member(ht1, 1)
    assert not ht_member(ht1, 2)

    # intersection
    inter = ht_intersection(ht1, ht2)
    assert ht_equals(inter, from_list([1, None]))

    # to_from_list
    assert to_list(ht1) == [1, None] or to_list(ht1) == [None, 1]
    assert ht_equals(ht1, from_list([1, None]))
    assert ht_equals(ht1, from_list([1, None, 1]))

    # concat
    combined = ht_concat(ht1, ht2)
    assert ht_equals(combined, from_list([None, 1, 1, None]))

    # iterator
    collected = []
    for item in ht_iterator(ht1):
        collected.append(item)
    assert ht_equals(from_list(collected), from_list([None, 1]))

    # filter
    numbers = from_list([1, 2, 3, 4])
    even = ht_filter(numbers, lambda x: x % 2 == 0)
    assert ht_equals(even, from_list([2, 4]))

    # map
    doubled = ht_map(numbers, lambda x: x * 2)
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


@given(st.lists(st.integers()))
def test_monoid_identity(b):
    ht = from_list(b)

    combined_left = ht_concat(ht_empty(), ht)
    assert ht_equals(combined_left, from_list(b))

    combined_right = ht_concat(ht, ht_empty())
    assert ht_equals(combined_right, from_list(b))


@given(
    a=st.lists(st.integers()),
    b=st.lists(st.integers()),
    c=st.lists(st.integers())
)
def test_monoid_associativity(a, b, c):
    ht_a = from_list(a)
    ht_b = from_list(b)
    ht_c = from_list(c)

    left = ht_concat(ht_concat(ht_a, ht_b), ht_c)
    right = ht_concat(ht_a, ht_concat(ht_b, ht_c))

    assert ht_equals(left, right)


@given(st.lists(st.integers(), unique=True))
def test_size_consistency(a):
    assert ht_size(from_list(a)) == len(a)


if __name__ == "__main__":
    pytest.main()
