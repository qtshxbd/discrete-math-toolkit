import math

import pytest

from discrete_math_toolkit import (
    chinese_remainder,
    euler_phi,
    extended_gcd,
    gcd,
    is_prime,
    lcm,
    mod_inverse,
    mod_pow,
    prime_factorization,
    sieve_of_eratosthenes,
)


def test_gcd_and_lcm_match_math_module():
    for a in range(-30, 31, 7):
        for b in range(0, 50, 3):
            assert gcd(a, b) == math.gcd(a, b)
            assert lcm(a, b) == math.lcm(a, b)


def test_extended_gcd_bezout_identity():
    for a, b in [(240, 46), (17, 5), (0, 9), (-35, 15), (101, 103)]:
        g, x, y = extended_gcd(a, b)
        assert g == math.gcd(a, b)
        assert a * x + b * y == g


def test_is_prime_agrees_with_sieve():
    primes = set(sieve_of_eratosthenes(10_000))
    for n in range(-5, 10_001):
        assert is_prime(n) == (n in primes)


@pytest.mark.parametrize(
    "n, expected",
    [
        (2**61 - 1, True),  # Mersenne prime
        (1_000_000_007, True),
        (561, False),  # Carmichael number: fools the Fermat test
        (3_215_031_751, False),  # strong pseudoprime to bases 2, 3, 5, 7
        ((2**31 - 1) * (2**61 - 1), False),
    ],
)
def test_is_prime_large_and_tricky_numbers(n, expected):
    assert is_prime(n) == expected


def test_sieve_small_values():
    assert sieve_of_eratosthenes(1) == []
    assert sieve_of_eratosthenes(2) == [2]
    assert sieve_of_eratosthenes(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert len(sieve_of_eratosthenes(1_000_000)) == 78_498


def test_prime_factorization():
    assert prime_factorization(1) == {}
    assert prime_factorization(360) == {2: 3, 3: 2, 5: 1}
    assert prime_factorization(97) == {97: 1}
    assert prime_factorization(2**10 * 7**3) == {2: 10, 7: 3}


def test_factorization_multiplies_back():
    for n in range(1, 2000):
        product = 1
        for p, e in prime_factorization(n).items():
            assert is_prime(p)
            product *= p**e
        assert product == n


def test_mod_pow_matches_builtin():
    for base, exp, mod in [(2, 10, 1000), (7, 222, 1001), (123456789, 10**18, 97), (5, 0, 13), (9, 4, 1)]:
        assert mod_pow(base, exp, mod) == pow(base, exp, mod)


def test_mod_pow_negative_exponent_uses_inverse():
    assert mod_pow(3, -1, 11) == 4  # 3 * 4 = 12 = 1 (mod 11)
    assert mod_pow(3, -2, 11) == pow(3, -2, 11)


def test_fermats_little_theorem():
    for p in sieve_of_eratosthenes(60):
        for a in range(1, p):
            assert mod_pow(a, p - 1, p) == 1


def test_mod_inverse():
    for a, m in [(3, 11), (10, 17), (7, 40), (-3, 11)]:
        assert a * mod_inverse(a, m) % m == 1


def test_mod_inverse_requires_coprime():
    with pytest.raises(ValueError):
        mod_inverse(6, 9)


def test_euler_phi():
    assert euler_phi(1) == 1
    assert euler_phi(9) == 6
    assert euler_phi(36) == 12
    for n in range(1, 200):
        assert euler_phi(n) == sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)


def test_eulers_theorem():
    n = 20
    for a in range(1, n):
        if math.gcd(a, n) == 1:
            assert mod_pow(a, euler_phi(n), n) == 1


def test_chinese_remainder_classic_example():
    # x = 2 (mod 3), x = 3 (mod 5), x = 2 (mod 7)
    assert chinese_remainder([2, 3, 2], [3, 5, 7]) == (23, 105)


def test_chinese_remainder_solution_satisfies_every_congruence():
    remainders, moduli = [1, 4, 6, 0], [4, 9, 11, 13]
    x, m = chinese_remainder(remainders, moduli)
    assert m == 4 * 9 * 11 * 13
    assert all(x % mod == r for r, mod in zip(remainders, moduli))


def test_chinese_remainder_rejects_non_coprime_moduli():
    with pytest.raises(ValueError):
        chinese_remainder([1, 2], [4, 6])
