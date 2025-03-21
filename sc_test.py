import hypothesis.strategies as st
import pytest
from hypothesis import given
from sc import (
    Node, cons, from_list, head, iterator,
    concat, empty, remove, reverse,
    size, tail, to_list, add, is_member,
    intersection, filter, map, reduce, equals, to_string
)


# Unit Tests
def test_size():
    assert size(None) == 0
    assert size(cons("a", None)) == 1
    assert size(cons("a", cons("b", None))) == 2


def test_cons():
    assert cons("a", None) == Node("a", None)
    assert cons("a", cons("b", None)) == Node("a", Node("b", None))


def test_remove():
    with pytest.raises(AssertionError):
        remove(None, "a")
    assert equals(remove(cons("a", None), "b"), cons("a", None))
    assert equals(remove(cons("a", cons("a", None)), "a"), cons("a", None))
    assert equals(remove(cons("a", cons("b", None)), "a"), cons("b", None))
    assert equals(remove(cons("a", cons("b", None)), "b"), cons("a", None))


def test_head():
    with pytest.raises(AssertionError):
        head(None)
    assert head(cons("a", None)) == "a"


def test_tail():
    with pytest.raises(AssertionError):
        tail(None)
    assert tail(cons("a", None)) is None
    assert tail(cons("a", cons("b", None))) == cons("b", None)


def test_reverse():
    assert reverse(None) is None
    assert reverse(cons("a", None)) == cons("a", None)
    assert reverse(cons("a", cons("b", None))) == cons("b", cons("a", None))


def test_concat():
    assert concat(None, None) is None
    assert concat(cons("a", None), None) == cons("a", None)
    assert concat(None, cons("a", None)) == cons("a", None)
    assert concat(cons("a", None), cons("b", None)) == cons("a", cons(
                                                                        "b",
                                                                        None
                                                                        ))
    assert concat(from_list([1, 2, 3]), from_list([4, 5, 6])) == from_list(
        [1, 2, 3, 4, 5, 6])


def test_to_list():
    assert to_list(None) == []
    assert to_list(cons("a", None)) == ["a"]
    assert to_list(cons("a", cons("b", None))) == ["a", "b"]


def test_from_list():
    test_data = [[], ["a"], ["a", "b"]]
    for e in test_data:
        assert to_list(from_list(e)) == e


def test_add():
    lst = from_list([1, 2, 3])
    new_lst = add(lst, 0)
    assert to_list(new_lst) == [0, 1, 2, 3]


def test_is_member():
    lst = from_list([1, 2, 3])
    assert is_member(lst, 2) is True
    assert is_member(lst, 4) is False


def test_intersection():
    lst1 = from_list([1, 2, 3])
    lst2 = from_list([2, 3, 4])
    inter = intersection(lst1, lst2)
    assert sorted(to_list(inter)) == [2, 3]


def test_filter():
    lst = from_list([1, 2, 3, 4])
    filtered = filter(lst, lambda x: x % 2 == 0)
    assert to_list(filtered) == [2, 4]


def test_map():
    lst = from_list([1, 2, 3])
    mapped = map(lst, lambda x: x * 2)
    assert to_list(mapped) == [2, 4, 6]


def test_reduce():
    lst = from_list([1, 2, 3, 4])
    result = reduce(lst, lambda acc, x: acc + x, 0)
    assert result == 10


def test_equals():
    lst1 = from_list([1, 2, 3])
    lst2 = from_list([1, 2, 3])
    lst3 = from_list([1, 2])
    assert equals(lst1, lst2) is True
    assert equals(lst1, lst3) is False


def test_to_string():
    assert to_string(None) == "Empty"
    assert to_string(from_list([1])) == "1"
    assert to_string(from_list([1, 2])) in ["1 : 2", "2 : 1"]


# Property-Based Tests
@given(st.lists(st.integers()))
def test_from_list_to_list_roundtrip(lst):
    assert to_list(from_list(lst)) == lst


@given(st.lists(st.integers()), st.integers())
def test_add_remove_property(lst, value):
    original = from_list(lst)
    added = add(original, value)
    removed = remove(added, value)

    if value not in lst:
        assert equals(removed, original)


@given(st.lists(st.integers()))
def test_reverse_property(lst):
    original = from_list(lst)
    reversed_once = reverse(original)
    reversed_twice = reverse(reversed_once)
    assert equals(reversed_twice, original)


@given(
        st.lists(st.integers()),
        st.lists(st.integers()),
        st.lists(st.integers())
        )
def test_monoid_associativity(a, b, c):
    list_a = from_list(a)
    list_b = from_list(b)
    list_c = from_list(c)

    left = concat(concat(list_a, list_b), list_c)
    right = concat(list_a, concat(list_b, list_c))
    assert equals(left, right)


@given(st.lists(st.integers()))
def test_size_property(lst):
    assert size(from_list(lst)) == len(lst)


@given(st.lists(st.integers()), st.integers())
def test_membership_property(lst, value):
    linked_list = from_list(lst)
    assert is_member(linked_list, value) == (value in lst)


def test_iterator():
    x = [1, 2, 3]
    lst = from_list(x)

    collected = []
    it = iterator(lst)
    try:
        while True:
            collected.append(it())
    except StopIteration:
        pass
    assert collected == x

    empty_it = iterator(None)
    with pytest.raises(StopIteration):
        empty_it()


def test_full_api():
    empty_list = empty()

    lst_with_none = cons(None, empty_list)
    assert to_string(lst_with_none) == "None"

    lst1 = cons(None, cons(1, empty_list))
    lst2 = cons(1, cons(None, empty_list))

    assert size(empty_list) == 0
    assert size(lst1) == 2

    inter = intersection(lst1, lst2)
    assert equals(inter, lst1)

    numbers = from_list([1, 2, 3, 4])
    even = filter(numbers, lambda x: x % 2 == 0)
    assert to_list(even) == [2, 4]

    collected = []
    it = iterator(lst1)
    try:
        while True:
            collected.append(it())
    except StopIteration:
        pass
    assert collected == [None, 1]


if __name__ == "__main__":
    pytest.main()
