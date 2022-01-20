def size(self, weight=None):
    s = sum(d for v, d in self.degree(weight=weight))
    return s // 2 if weight is None else s / 2


def order(self):
    return len(self._node)


def density(G):
    n = number_of_nodes(G)
    m = number_of_edges(G)
    if m == 0 or n <= 1:
        return 0
    d = m / (n * (n - 1))
    if not G.is_directed():
        d *= 2
    return d


def best_partition(
    graph,
    partition=None,
    weight="weight",
    resolution=1.0,
    randomize=None,
    random_state=None,
):
    dendo = generate_dendrogram(
        graph, partition, weight, resolution, randomize, random_state
    )
    return partition_at_level(dendo, len(dendo) - 1)


def modularity(partition, graph, weight="weight"):
    if graph.is_directed():
        raise TypeError("Bad graph type, use only non directed graph")

    inc = dict([])
    deg = dict([])
    links = graph.size(weight=weight)
    if links == 0:
        raise ValueError("A graph without link has an undefined modularity")

    for node in graph:
        com = partition[node]
        deg[com] = deg.get(com, 0.0) + graph.degree(node, weight=weight)
        for neighbor, datas in graph[node].items():
            edge_weight = datas.get(weight, 1)
            if partition[neighbor] == com:
                if neighbor == node:
                    inc[com] = inc.get(com, 0.0) + float(edge_weight)
                else:
                    inc[com] = inc.get(com, 0.0) + float(edge_weight) / 2.0

    res = 0.0
    for com in set(partition.values()):
        res += (inc.get(com, 0.0) / links) - (deg.get(com, 0.0) / (2.0 * links)) ** 2
    return res


def all_pairs_shortest_path_length(G, cutoff=None):
    length = single_source_shortest_path_length
    # TODO This can be trivially parallelized.
    for n in G:
        yield (n, dict(length(G, n, cutoff=cutoff)))


def single_source_shortest_path_length(G, source, cutoff=None):
    if source not in G:
        raise nx.NodeNotFound("Source {} is not in G".format(source))
    if cutoff is None:
        cutoff = float("inf")
    nextlevel = {source: 1}
    return _single_shortest_path_length(G.adj, nextlevel, cutoff)


def _single_shortest_path_length(adj, firstlevel, cutoff):
    """Yields (node, level) in a breadth first search"""
    seen = {}  # level (number of hops) when seen in BFS
    level = 0  # the current level
    nextlevel = firstlevel  # dict of nodes to check at next level

    while nextlevel and cutoff >= level:
        thislevel = nextlevel  # advance to next level
        nextlevel = {}  # and start a new list (fringe)
        for v in thislevel:
            if v not in seen:
                seen[v] = level  # set the level of vertex v
                nextlevel.update(adj[v])  # add neighbors of v
                yield (v, level)
        level += 1
    del seen


def connected_components(G):
    seen = set()
    for v in G:
        if v not in seen:
            c = _plain_bfs(G, v)
            seen.update(c)
            yield c


def number_connected_components(G):
    return sum(1 for cc in connected_components(G))


def degree_centrality(G):
    if len(G) <= 1:
        return {n: 1 for n in G}

    s = 1.0 / (len(G) - 1.0)
    centrality = {n: d * s for n, d in G.degree()}
    return centrality


def betweenness_centrality(
    G, k=None, normalized=True, weight=None, endpoints=False, seed=None
):
    betweenness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    if k is None:
        nodes = G
    else:
        random.seed(seed)
        nodes = random.sample(G.nodes(), k)
    for s in nodes:
        # single source shortest paths
        if weight is None:  # use BFS
            S, P, sigma = _single_source_shortest_path_basic(G, s)
        else:  # use Dijkstra's algorithm
            S, P, sigma = _single_source_dijkstra_path_basic(G, s, weight)
        # accumulation
        if endpoints:
            betweenness = _accumulate_endpoints(betweenness, S, P, sigma, s)
        else:
            betweenness = _accumulate_basic(betweenness, S, P, sigma, s)
    # rescaling
    betweenness = _rescale(
        betweenness, len(G), normalized=normalized, directed=G.is_directed(), k=k
    )
    return betweenness
