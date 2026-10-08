# Discrete Math Toolkit

[![tests](https://github.com/qtshxbd/discrete-math-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/qtshxbd/discrete-math-toolkit/actions/workflows/tests.yml)

Core results from discrete mathematics implemented from first principles in Python. It covers counting and the pigeonhole principle, graph traversal and cycle detection, and primality and modular arithmetic. Each algorithm is written out rather than wrapped from a library, and a pytest suite checks it against brute force, the standard library, and known mathematical identities.

## What's inside

**`combinatorics`**
- `factorial`, `permutations`, `combinations` (exact integer arithmetic, no floating point)
- `permutations_with_repetition`, `combinations_with_repetition` (stars and bars), `multinomial`, `pascal_row`
- `generate_combinations`, `generate_permutations`: backtracking generators
- `pigeonhole_guaranteed`, `pigeonhole_items_needed`, `find_pigeonhole_collision`

**`graphs`**
- `Graph`: adjacency-list graph, directed or undirected
- `bfs`, `dfs` (iterative, so no recursion limit), `shortest_path` (unweighted, via BFS)
- `has_cycle`: union-find for undirected graphs, three-color DFS for directed graphs
- `connected_components`, `topological_sort` (Kahn's algorithm), `is_bipartite`

**`number_theory`**
- `gcd`, `extended_gcd` (Bézout coefficients), `lcm`
- `is_prime`: deterministic Miller–Rabin, exact for n < 3.3 × 10²⁴
- `sieve_of_eratosthenes`, `prime_factorization`, `euler_phi`
- `mod_pow` (square-and-multiply), `mod_inverse`, `chinese_remainder`

## Quick start

```bash
git clone https://github.com/qtshxbd/discrete-math-toolkit.git
cd discrete-math-toolkit
pip install -e ".[test]"
python examples/demo.py
```

```python
from discrete_math_toolkit import Graph, shortest_path, has_cycle, combinations, is_prime

combinations(52, 5)                 # 2598960 poker hands
is_prime(561)                       # False: a Carmichael number, caught by Miller-Rabin

g = Graph.from_edges([("A", "B"), ("B", "C"), ("A", "C")])
shortest_path(g, "A", "C")          # ['A', 'C']
has_cycle(g)                        # True
```

## Demo output

`python examples/demo.py`:

```
== Combinatorics ==
5-card poker hands: 2,598,960
Arrangements of MISSISSIPPI: 34,650
Socks to draw (4 colors) to guarantee a pair: 5
Two of six numbers share a remainder mod 5: (22, 37)

== Graphs ==
BFS from Dorm: ['Dorm', 'Library', 'Cafe', 'Lab', 'Gym']
DFS from Dorm: ['Dorm', 'Library', 'Lab', 'Gym', 'Cafe']
Shortest route Dorm -> Lab: ['Dorm', 'Library', 'Lab']
Campus loop exists: True
Course order: ['Calc I', 'Discrete Math', 'Calc II', 'Linear Algebra', 'Numerical Analysis']

== Number theory ==
2^61 - 1 is prime: True
561 is prime: False (factors: {3: 1, 11: 1, 17: 1})
Inverse of 17 mod 3120: 2753
x = 2 (mod 3), 3 (mod 5), 2 (mod 7)  ->  x = 23 (mod 105)
```

## Design notes

- **Cycle detection depends on direction.** In an undirected graph, union-find flags a cycle the moment an edge connects two vertices that are already connected. In a directed graph that test gives wrong answers: a "diamond" A→B, A→C, B→D, C→D has no directed cycle. So directed graphs use DFS with white/gray/black coloring, where reaching a gray vertex (one still on the current path) means a back edge.
- **Miller–Rabin instead of trial division.** Trial division takes about √n steps, which is far too slow for numbers like 2⁶¹ − 1. Testing a fixed set of prime bases makes Miller–Rabin both fast and exact in its stated range. The suite includes inputs that fool weaker tests, such as the Carmichael number 561 and the strong pseudoprime 3,215,031,751.
- **Pigeonhole as an algorithm.** `find_pigeonhole_collision` turns the existence proof into a one-pass search: with more items than boxes, a collision is guaranteed, and a hash map finds one in O(n).

## Testing

```bash
pytest
```

Tests compare every function with an independent source of truth: Python's `math` module and `itertools`, brute-force counting, or identities such as Fermat's little theorem, Euler's theorem, Bézout's identity, and Pascal's triangle summing to 2ⁿ. GitHub Actions runs the suite on Python 3.9 through 3.12 for every push.

## License

MIT
