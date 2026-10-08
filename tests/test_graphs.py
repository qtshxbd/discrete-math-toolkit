import pytest

from discrete_math_toolkit import (
    Graph,
    bfs,
    connected_components,
    dfs,
    has_cycle,
    is_bipartite,
    shortest_path,
    topological_sort,
)


@pytest.fixture
def tree():
    #       1
    #     /   \
    #    2     3
    #   / \     \
    #  4   5     6
    return Graph.from_edges([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)])


def test_graph_basics(tree):
    assert len(tree) == 6
    assert 4 in tree and 99 not in tree
    assert tree.neighbors(2) == [1, 4, 5]
    assert len(tree.edges) == 5


def test_duplicate_edges_are_ignored():
    g = Graph.from_edges([("a", "b"), ("b", "a"), ("a", "b")])
    assert len(g.edges) == 1
    assert not has_cycle(g)


def test_bfs_visits_level_by_level(tree):
    assert bfs(tree, 1) == [1, 2, 3, 4, 5, 6]


def test_dfs_goes_deep_first(tree):
    assert dfs(tree, 1) == [1, 2, 4, 5, 3, 6]


def test_traversals_only_reach_connected_vertices():
    g = Graph.from_edges([(1, 2), (3, 4)])
    assert set(bfs(g, 1)) == {1, 2}
    assert set(dfs(g, 3)) == {3, 4}


def test_dfs_handles_long_paths_without_recursion_limit():
    n = 5000
    g = Graph.from_edges((i, i + 1) for i in range(n))
    assert len(dfs(g, 0)) == n + 1


def test_shortest_path_finds_fewest_edges():
    # Two routes from A to E: A-B-C-D-E (4 edges) and A-F-E (2 edges).
    g = Graph.from_edges([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("A", "F"), ("F", "E")])
    assert shortest_path(g, "A", "E") == ["A", "F", "E"]
    assert shortest_path(g, "A", "A") == ["A"]


def test_shortest_path_unreachable_returns_none():
    g = Graph.from_edges([(1, 2), (3, 4)])
    assert shortest_path(g, 1, 4) is None


def test_shortest_path_respects_direction():
    g = Graph.from_edges([(1, 2), (2, 3)], directed=True)
    assert shortest_path(g, 1, 3) == [1, 2, 3]
    assert shortest_path(g, 3, 1) is None


def test_undirected_cycle_detection(tree):
    assert not has_cycle(tree)
    tree.add_edge(5, 6)
    assert has_cycle(tree)


def test_self_loop_is_a_cycle():
    g = Graph.from_edges([(1, 1)])
    assert has_cycle(g)
    assert has_cycle(Graph.from_edges([(1, 1)], directed=True))


def test_directed_cycle_detection():
    dag = Graph.from_edges([(1, 2), (2, 3), (1, 3)], directed=True)
    assert not has_cycle(dag)  # a diamond is not a directed cycle
    dag.add_edge(3, 1)
    assert has_cycle(dag)


def test_connected_components():
    g = Graph.from_edges([(1, 2), (2, 3), (4, 5)])
    g.add_vertex(6)
    components = connected_components(g)
    assert sorted(map(sorted, components)) == [[1, 2, 3], [4, 5], [6]]


def test_topological_sort_respects_every_edge():
    # Course prerequisites.
    edges = [
        ("Calc I", "Calc II"),
        ("Calc II", "Multivariable"),
        ("Calc II", "Linear Algebra"),
        ("Discrete Math", "Linear Algebra"),
        ("Linear Algebra", "Numerical Analysis"),
    ]
    g = Graph.from_edges(edges, directed=True)
    order = topological_sort(g)
    position = {course: i for i, course in enumerate(order)}
    assert len(order) == len(g)
    assert all(position[u] < position[v] for u, v in edges)


def test_topological_sort_rejects_cycles():
    g = Graph.from_edges([(1, 2), (2, 3), (3, 1)], directed=True)
    with pytest.raises(ValueError):
        topological_sort(g)


def test_bipartite():
    even_cycle = Graph.from_edges([(1, 2), (2, 3), (3, 4), (4, 1)])
    odd_cycle = Graph.from_edges([(1, 2), (2, 3), (3, 1)])
    assert is_bipartite(even_cycle)
    assert not is_bipartite(odd_cycle)


def test_algorithms_reject_wrong_graph_type():
    with pytest.raises(ValueError):
        connected_components(Graph(directed=True))
    with pytest.raises(ValueError):
        topological_sort(Graph())
    with pytest.raises(ValueError):
        is_bipartite(Graph(directed=True))


def test_missing_vertex_raises(tree):
    with pytest.raises(KeyError):
        bfs(tree, 42)
    with pytest.raises(KeyError):
        dfs(tree, 42)
    with pytest.raises(KeyError):
        tree.neighbors(42)
