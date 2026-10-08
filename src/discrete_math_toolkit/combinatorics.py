"""Counting: factorials, permutations, combinations, and the pigeonhole principle."""

from __future__ import annotations

from collections.abc import Callable, Hashable, Iterable, Iterator, Sequence
from typing import Any, TypeVar

T = TypeVar("T")


def _check_nonnegative_int(**values: int) -> None:
    for name, value in values.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer")


def factorial(n: int) -> int:
    """n! computed iteratively."""
    _check_nonnegative_int(n=n)
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def permutations(n: int, k: int) -> int:
    """P(n, k) = n! / (n - k)!: ordered selections of k items from n."""
    _check_nonnegative_int(n=n, k=k)
    if k > n:
        return 0
    result = 1
    for i in range(n - k + 1, n + 1):
        result *= i
    return result


def combinations(n: int, k: int) -> int:
    """C(n, k) = n! / (k! (n - k)!): unordered selections of k items from n.

    Uses the multiplicative formula on the smaller of k and n - k, so every
    intermediate result is an exact integer.
    """
    _check_nonnegative_int(n=n, k=k)
    if k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result


def permutations_with_repetition(n: int, k: int) -> int:
    """Sequences of length k drawn from n symbols, repeats allowed: n^k."""
    _check_nonnegative_int(n=n, k=k)
    return n**k


def combinations_with_repetition(n: int, k: int) -> int:
    """Multisets of size k from n types ("stars and bars"): C(n + k - 1, k)."""
    _check_nonnegative_int(n=n, k=k)
    if n == 0:
        return 1 if k == 0 else 0
    return combinations(n + k - 1, k)


def multinomial(*counts: int) -> int:
    """Arrangements of a multiset, e.g. multinomial(1, 4, 4, 2) for MISSISSIPPI."""
    _check_nonnegative_int(**{f"count_{i}": c for i, c in enumerate(counts)})
    result = 1
    total = 0
    for count in counts:
        total += count
        result *= combinations(total, count)
    return result


def pascal_row(n: int) -> list[int]:
    """Row n of Pascal's triangle, built additively from the previous row."""
    _check_nonnegative_int(n=n)
    row = [1]
    for _ in range(n):
        row = [1] + [a + b for a, b in zip(row, row[1:])] + [1]
    return row


def generate_combinations(items: Sequence[T], k: int) -> Iterator[tuple[T, ...]]:
    """Yield every k-element combination of `items` in lexicographic index order (backtracking)."""
    _check_nonnegative_int(k=k)
    chosen: list[T] = []

    def backtrack(start: int) -> Iterator[tuple[T, ...]]:
        if len(chosen) == k:
            yield tuple(chosen)
            return
        # Stop early once too few items remain to finish the combination.
        for i in range(start, len(items) - (k - len(chosen)) + 1):
            chosen.append(items[i])
            yield from backtrack(i + 1)
            chosen.pop()

    yield from backtrack(0)


def generate_permutations(items: Sequence[T]) -> Iterator[tuple[T, ...]]:
    """Yield every ordering of `items` by swapping elements in place (backtracking)."""
    pool = list(items)

    def backtrack(first: int) -> Iterator[tuple[T, ...]]:
        if first == len(pool):
            yield tuple(pool)
            return
        for i in range(first, len(pool)):
            pool[first], pool[i] = pool[i], pool[first]
            yield from backtrack(first + 1)
            pool[first], pool[i] = pool[i], pool[first]

    yield from backtrack(0)


def pigeonhole_guaranteed(items: int, boxes: int) -> int:
    """The fullest box must hold at least ceil(items / boxes) items."""
    _check_nonnegative_int(items=items)
    if boxes < 1:
        raise ValueError("boxes must be at least 1")
    return -(-items // boxes)


def pigeonhole_items_needed(boxes: int, target: int) -> int:
    """Smallest number of items that forces some box to hold at least `target`.

    Each box can take target - 1 items without reaching the target, so one
    more item than boxes * (target - 1) guarantees it.
    """
    if boxes < 1 or target < 1:
        raise ValueError("boxes and target must be at least 1")
    return boxes * (target - 1) + 1


def find_pigeonhole_collision(
    items: Iterable[T], box_of: Callable[[T], Hashable]
) -> tuple[T, T] | None:
    """Return the first two items that land in the same box, or None.

    The pigeonhole principle promises a collision whenever there are more
    items than possible boxes; this finds one in a single pass.
    """
    seen: dict[Any, T] = {}
    for item in items:
        box = box_of(item)
        if box in seen:
            return seen[box], item
        seen[box] = item
    return None
