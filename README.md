# Nikki - lab 2 - variant 4

A series of functional requirements are realized and tested based on
`hash map, separate chaining` method.

## Project structure

- `sc.py` -- Implementation of immutable algorithms based on hash map

with separate chaining.

  Supports methods: `empty`, `cons`, `head`, `tail`, `add`, `remove`,
  `size`, `is_member`, `reverse`, `intersection`, `to_list`, `from_list`,
   `find`, `filter`, `map`, `reduce`, `iterator`, `concat`, `equals`, `to_string`.
- `sc_test.py` -- Unit and property-based tests for `sc`.

## Features

- **PBT Tests**:
   - `test_from_list_to_list_roundtrip`
   - `test_add_remove_property`
   - `test_reverse_property`
   - `test_monoid_associativity`
   - `test_size_property`
   - `test_membership_property`

## Contribution

- **Lei Ningyu** (3232254146@qq.com) -- Implementation and testing.
- **Yi Min** (1757973489@qq.com) -- Implementation and testing.

## Changelog

- **12.03.2025 - v0**
   - Initial version.
- **14.03.2025 - v1**
   - Updated README, `sc.py`, and `sc_test.py`.
- **16.03.2025 - v2**
   - Revised README and modified `sc.py`, `sc_test.py`.
- **19.03.2025 - v3**
   - Finalized README and code optimizations.
- **21.03.2025 - v4**
   - Revised README and modified `sc.py`, `sc_test.py`.

## Design Notes

- **Separate Chaining Hash Map**:
   - Each bucket (array index) stores a linked list of key-value pairs.
   - Hash value modulo capacity determines the bucket index.
   - Duplicate values are rejected within the same bucket.

- **Sorted Operation**:
   - When we use sorted in our API tests, we find that it cannot sort
   different types of data.
   - Correct approach: All sorted functions with data of different
   types are deleted.

- **Compare mutable and immutable implementations**:
   - Mutable: Allows in situ modification, memory address unchanged, saving memory.
   - Immutable: New objects are generated with each modification, and
   old objects are retained.
