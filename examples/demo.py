"""A short tour of the toolkit: counting, graphs, and number theory."""

from discrete_math_toolkit import (
    Graph,
    bfs,
    chinese_remainder,
    combinations,
    dfs,
    find_pigeonhole_collision,
    has_cycle,
    is_prime,
    mod_inverse,
    multinomial,
    pigeonhole_items_needed,
    prime_factorization,
    shortest_path,
    topological_sort,
)


def counting() -> None:
    print("== Combinatorics ==")
    print(f"5-card poker hands: {combinations(52, 5):,}")
    print(f"Arrangements of MISSISSIPPI: {multinomial(1, 4, 4, 2):,}")
    print(f"Socks to draw (4 colors) to guarantee a pair: {pigeonhole_items_needed(4, 2)}")
    pair = find_pigeonhole_collision([14, 22, 37, 51, 60, 83], lambda n: n % 5)
    print(f"Two of six numbers share a remainder mod 5: {pair}")


def graphs() -> None:
    print("\n== Graphs ==")
    campus = Graph.from_edges(
        [("Dorm", "Library"), ("Library", "Lab"), ("Lab", "Gym"), ("Dorm", "Cafe"), ("Cafe", "Gym")]
    )
    print(f"BFS from Dorm: {bfs(campus, 'Dorm')}")
    print(f"DFS from Dorm: {dfs(campus, 'Dorm')}")
    print(f"Shortest route Dorm -> Lab: {shortest_path(campus, 'Dorm', 'Lab')}")
    print(f"Campus loop exists: {has_cycle(campus)}")

    prereqs = Graph.from_edges(
        [
            ("Calc I", "Calc II"),
            ("Calc II", "Linear Algebra"),
            ("Discrete Math", "Linear Algebra"),
            ("Linear Algebra", "Numerical Analysis"),
        ],
        directed=True,
    )
    print(f"Course order: {topological_sort(prereqs)}")


def number_theory() -> None:
    print("\n== Number theory ==")
    print(f"2^61 - 1 is prime: {is_prime(2**61 - 1)}")
    print(f"561 is prime: {is_prime(561)} (factors: {prime_factorization(561)})")
    print(f"Inverse of 17 mod 3120: {mod_inverse(17, 3120)}")
    x, m = chinese_remainder([2, 3, 2], [3, 5, 7])
    print(f"x = 2 (mod 3), 3 (mod 5), 2 (mod 7)  ->  x = {x} (mod {m})")


if __name__ == "__main__":
    counting()
    graphs()
    number_theory()
