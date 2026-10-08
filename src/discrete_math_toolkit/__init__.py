"""Discrete Math Toolkit: combinatorics, graph algorithms, and number theory."""

from .combinatorics import (
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
from .graphs import (
    Graph,
    bfs,
    connected_components,
    dfs,
    has_cycle,
    is_bipartite,
    shortest_path,
    topological_sort,
)
from .number_theory import (
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

__version__ = "1.0.0"
