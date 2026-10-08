"""Number theory: divisibility, primes, and modular arithmetic."""

from __future__ import annotations


def gcd(a: int, b: int) -> int:
    """Greatest common divisor by the Euclidean algorithm."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with g = gcd(a, b) and a*x + b*y = g (Bezout coefficients)."""
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    if old_r < 0:
        old_r, old_x, old_y = -old_r, -old_x, -old_y
    return old_r, old_x, old_y


def lcm(a: int, b: int) -> int:
    """Least common multiple, using lcm(a, b) * gcd(a, b) = |a * b|."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


# Testing these bases makes Miller-Rabin exact for every n < 3.3 * 10^24.
_MILLER_RABIN_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)


def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin primality test (exact for n < 3.3 * 10^24)."""
    if n < 2:
        return False
    for p in _MILLER_RABIN_BASES:
        if n % p == 0:
            return n == p
    # Write n - 1 = d * 2^s with d odd.
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _MILLER_RABIN_BASES:
        x = mod_pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False  # a is a witness that n is composite
    return True


def sieve_of_eratosthenes(limit: int) -> list[int]:
    """All primes up to and including `limit`."""
    if limit < 2:
        return []
    is_candidate = [True] * (limit + 1)
    is_candidate[0] = is_candidate[1] = False
    p = 2
    while p * p <= limit:
        if is_candidate[p]:
            # Smaller multiples were already crossed off by smaller primes.
            for multiple in range(p * p, limit + 1, p):
                is_candidate[multiple] = False
        p += 1
    return [i for i, prime in enumerate(is_candidate) if prime]


def prime_factorization(n: int) -> dict[int, int]:
    """Map each prime factor of n to its exponent, e.g. 360 -> {2: 3, 3: 2, 5: 1}."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    factors: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def mod_pow(base: int, exponent: int, modulus: int) -> int:
    """base^exponent mod modulus by repeated squaring, in O(log exponent) steps."""
    if modulus < 1:
        raise ValueError("modulus must be positive")
    if exponent < 0:
        return mod_pow(mod_inverse(base, modulus), -exponent, modulus)
    result = 1 % modulus
    base %= modulus
    while exponent:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return result


def mod_inverse(a: int, modulus: int) -> int:
    """x with a*x = 1 (mod modulus); exists only when gcd(a, modulus) = 1."""
    if modulus < 1:
        raise ValueError("modulus must be positive")
    g, x, _ = extended_gcd(a % modulus, modulus)
    if g != 1:
        raise ValueError(f"{a} has no inverse modulo {modulus} (gcd is {g})")
    return x % modulus


def euler_phi(n: int) -> int:
    """Count of integers in [1, n] coprime to n, via n * product(1 - 1/p)."""
    result = n
    for p in prime_factorization(n):
        result -= result // p
    return result


def chinese_remainder(remainders: list[int], moduli: list[int]) -> tuple[int, int]:
    """Solve x = r_i (mod m_i) for pairwise-coprime moduli.

    Returns (x, M) where M is the product of the moduli and 0 <= x < M.
    """
    if len(remainders) != len(moduli) or not moduli:
        raise ValueError("need the same, non-zero number of remainders and moduli")
    x, m = 0, 1
    for r_i, m_i in zip(remainders, moduli):
        if m_i < 1:
            raise ValueError("moduli must be positive")
        if gcd(m, m_i) != 1:
            raise ValueError("moduli must be pairwise coprime")
        # Choose t so that x + m*t = r_i (mod m_i).
        t = (r_i - x) * mod_inverse(m, m_i) % m_i
        x += m * t
        m *= m_i
    return x % m, m
