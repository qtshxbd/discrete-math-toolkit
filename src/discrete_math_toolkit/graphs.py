"""Graph representation and classic traversal algorithms (BFS, DFS, cycles, ordering)."""

from __future__ import annotations

from collections import deque
from collections.abc import Hashable, Iterator

Vertex = Hashable


class Graph:
    """A simple graph stored as an adjacency list.

    Undirected by default. Duplicate edges are ignored so the graph stays simple;
    self-loops are allowed and count as cycles.
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self._adj: dict[Vertex, list[Vertex]] = {}
        self._edges: list[tuple[Vertex, Vertex]] = []

    @classmethod
    def from_edges(cls, edges, directed: bool = False) -> "Graph":
        graph = cls(directed=directed)
        for u, v in edges:
            graph.add_edge(u, v)
        return graph

    def add_vertex(self, v: Vertex) -> None:
        self._adj.setdefault(v, [])

    def add_edge(self, u: Vertex, v: Vertex) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        if v in self._adj[u]:
            return
        self._adj[u].append(v)
        if not self.directed and u != v:
            self._adj[v].append(u)
        self._edges.append((u, v))

    def neighbors(self, v: Vertex) -> list[Vertex]:
        if v not in self._adj:
            raise KeyError(f"vertex {v!r} is not in the graph")
        return list(self._adj[v])

    @property
    def vertices(self) -> list[Vertex]:
        return list(self._adj)

    @property
    def edges(self) -> list[tuple[Vertex, Vertex]]:
        return list(self._edges)

    def __contains__(self, v: object) -> bool:
        return v in self._adj

    def __len__(self) -> int:
        return len(self._adj)

    def __iter__(self) -> Iterator[Vertex]:
        return iter(self._adj)


def bfs(graph: Graph, start: Vertex) -> list[Vertex]:
    """Breadth-first order of the vertices reachable from `start`."""
    if start not in graph:
        raise KeyError(f"vertex {start!r} is not in the graph")
    visited = {start}
    order = []
    queue = deque([start])
    while queue:
        v = queue.popleft()
        order.append(v)
        for w in graph.neighbors(v):
            if w not in visited:
                visited.add(w)
                queue.append(w)
    return order


def dfs(graph: Graph, start: Vertex) -> list[Vertex]:
    """Depth-first (preorder) order of vertices reachable from `start`.

    Iterative with an explicit stack, so deep graphs don't hit Python's
    recursion limit. Neighbors are explored in insertion order.
    """
    if start not in graph:
        raise KeyError(f"vertex {start!r} is not in the graph")
    visited = set()
    order = []
    stack = [start]
    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        order.append(v)
        # Push in reverse so the first neighbor is explored first.
        for w in reversed(graph.neighbors(v)):
            if w not in visited:
                stack.append(w)
    return order


def shortest_path(graph: Graph, start: Vertex, goal: Vertex) -> list[Vertex] | None:
    """Fewest-edges path from `start` to `goal` using BFS, or None if unreachable."""
    if start not in graph or goal not in graph:
        raise KeyError("start and goal must both be in the graph")
    parent: dict[Vertex, Vertex] = {start: start}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        if v == goal:
            # Walk the parent links back to the start, then reverse.
            path = [v]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return path[::-1]
        for w in graph.neighbors(v):
            if w not in parent:
                parent[w] = v
                queue.append(w)
    return None


class _DisjointSet:
    """Union-find with path compression and union by size."""

    def __init__(self) -> None:
        self.parent: dict[Vertex, Vertex] = {}
        self.size: dict[Vertex, int] = {}

    def find(self, x: Vertex) -> Vertex:
        self.parent.setdefault(x, x)
        self.size.setdefault(x, 1)
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: Vertex, b: Vertex) -> bool:
        """Merge the sets holding a and b; return False if they were already joined."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def has_cycle(graph: Graph) -> bool:
    """Whether the graph contains a cycle.

    Undirected graphs use union-find: an edge whose endpoints are already
    connected closes a cycle. Directed graphs use three-color DFS: reaching a
    vertex that is still on the current path (gray) means a back edge.
    """
    if not graph.directed:
        components = _DisjointSet()
        return any(not components.union(u, v) for u, v in graph.edges)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph}
    for root in graph:
        if color[root] != WHITE:
            continue
        color[root] = GRAY
        stack = [(root, iter(graph.neighbors(root)))]
        while stack:
            v, children = stack[-1]
            for w in children:
                if color[w] == GRAY:
                    return True
                if color[w] == WHITE:
                    color[w] = GRAY
                    stack.append((w, iter(graph.neighbors(w))))
                    break
            else:
                color[v] = BLACK
                stack.pop()
    return False


def connected_components(graph: Graph) -> list[set[Vertex]]:
    """Connected components of an undirected graph, each as a set of vertices."""
    if graph.directed:
        raise ValueError("connected_components expects an undirected graph")
    seen: set[Vertex] = set()
    components = []
    for v in graph:
        if v not in seen:
            component = set(bfs(graph, v))
            seen |= component
            components.append(component)
    return components


def topological_sort(graph: Graph) -> list[Vertex]:
    """Order a directed acyclic graph so every edge points forward (Kahn's algorithm)."""
    if not graph.directed:
        raise ValueError("topological_sort expects a directed graph")
    in_degree = {v: 0 for v in graph}
    for _, v in graph.edges:
        in_degree[v] += 1
    queue = deque(v for v in graph if in_degree[v] == 0)
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for w in graph.neighbors(v):
            in_degree[w] -= 1
            if in_degree[w] == 0:
                queue.append(w)
    if len(order) != len(graph):
        raise ValueError("graph has a cycle, so no topological order exists")
    return order


def is_bipartite(graph: Graph) -> bool:
    """Whether an undirected graph's vertices can be 2-colored with no edge inside a color."""
    if graph.directed:
        raise ValueError("is_bipartite expects an undirected graph")
    side: dict[Vertex, int] = {}
    for root in graph:
        if root in side:
            continue
        side[root] = 0
        queue = deque([root])
        while queue:
            v = queue.popleft()
            for w in graph.neighbors(v):
                if w not in side:
                    side[w] = 1 - side[v]
                    queue.append(w)
                elif side[w] == side[v]:
                    return False
    return True
