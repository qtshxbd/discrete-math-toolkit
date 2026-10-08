import itertools
import math

import pytest

from discrete_math_toolkit import (
    combinations,
    combinations_with_repetition,
    factorial,
    find_pigeonhole_collision,
    generate_combinations,
    generate_permutations,
    multinomial,
    pascal_row,
    permutations,
    permutations_with_repetition,
    pigeonhole_guaranteed,
    pigeonhole_items_needed,
)


@pytest.mark.parametrize("n", [0, 1, 5, 10, 20])
def test_factorial_matches_math_module(n):
    assert factorial(n) == math.factorial(n)


def test_permutations_and_combinations_match_math_module():
    for n in range(0, 15):
        for k in range(0, n + 3):
            assert permutations(n, k) == math.perm(n, k)
            assert combinations(n, k) == math.comb(n, k)


def test_combinations_stay_exact_for_large_inputs():
    assert combinations(100, 50) == math.comb(100, 50)


def test_choose_k_greater_than_n_is_zero():
    assert combinations(3, 5) == 0
    assert permutations(3, 5) == 0


def test_repetition_counts():
    assert permutations_with_repetition(10, 4) == 10_000  # 4-digit PINs
    assert combinations_with_repetition(3, 2) == 6  # {aa, ab, ac, bb, bc, cc}
    assert combinations_with_repetition(0, 0) == 1
    assert combinations_with_repetition(0, 3) == 0


def test_combinations_with_repetition_matches_brute_force():
    brute = len(list(itertools.combinations_with_replacement(range(5), 3)))
    assert combinations_with_repetition(5, 3) == brute


def test_multinomial_mississippi():
    # M, I x4, S x4, P x2
    assert multinomial(1, 4, 4, 2) == 34_650


def test_pascal_row_values_and_sum():
    assert pascal_row(0) == [1]
    assert pascal_row(5) == [1, 5, 10, 10, 5, 1]
    for n in range(12):
        row = pascal_row(n)
        assert sum(row) == 2**n
        assert row == [combinations(n, k) for k in range(n + 1)]


def test_generate_combinations_matches_itertools():
    items = "abcde"
    for k in range(0, 6):
        assert list(generate_combinations(items, k)) == list(itertools.combinations(items, k))


def test_generate_permutations_produces_all_distinct_orderings():
    result = list(generate_permutations([1, 2, 3, 4]))
    assert len(result) == factorial(4)
    assert set(result) == set(itertools.permutations([1, 2, 3, 4]))


def test_generate_permutations_of_empty_sequence():
    assert list(generate_permutations([])) == [()]


def test_pigeonhole_guaranteed():
    assert pigeonhole_guaranteed(13, 12) == 2  # 13 people, 12 birth months
    assert pigeonhole_guaranteed(100, 7) == 15
    assert pigeonhole_guaranteed(12, 12) == 1


def test_pigeonhole_items_needed():
    # Socks in 4 colors: 5 draws guarantee a matching pair.
    assert pigeonhole_items_needed(4, 2) == 5
    assert pigeonhole_items_needed(12, 3) == 25


def test_items_needed_is_tight():
    boxes, target = 6, 4
    needed = pigeonhole_items_needed(boxes, target)
    assert pigeonhole_guaranteed(needed, boxes) == target
    assert pigeonhole_guaranteed(needed - 1, boxes) == target - 1


def test_find_collision_guaranteed_when_items_exceed_boxes():
    # Any 6 integers include two with the same remainder mod 5.
    pair = find_pigeonhole_collision([3, 11, 24, 7, 30, 19], lambda x: x % 5)
    assert pair is not None
    a, b = pair
    assert a % 5 == b % 5


def test_find_collision_returns_none_when_all_boxes_distinct():
    assert find_pigeonhole_collision([0, 1, 2, 3], lambda x: x % 5) is None


@pytest.mark.parametrize("bad", [-1, 2.5, True])
def test_rejects_invalid_counts(bad):
    with pytest.raises(ValueError):
        factorial(bad)


def test_pigeonhole_rejects_zero_boxes():
    with pytest.raises(ValueError):
        pigeonhole_guaranteed(5, 0)
    with pytest.raises(ValueError):
        pigeonhole_items_needed(0, 2)
