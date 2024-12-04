from .indexed_pq import IndexedMinPQ


def dijkstra_sp(G, src):
    """
    Implementation of Dijkstra's algorithm for finding the shortest path in a graph.

    Args:
        G: A graph compatible with networkx.
        src: The source vertex.

    Returns:
        dist_to: A dictionary of distances from src to each vertex.
        edge_to: A dictionary containing edges leading to each vertex.
    """
    if src not in G:
        raise ValueError(f"Source node {src} not in graph.")

    N = G.number_of_nodes()
    inf = float("inf")

    # Initialize distances
    dist_to = {v: inf for v in G.nodes()}
    dist_to[src] = 0

    # Initialize the IndexedMinPQ
    impq = IndexedMinPQ(N)
    impq.enqueue(src, dist_to[src])

    edge_to = {}

    def relax(edge):
        """
        Relax an edge. If a shorter path is found, update the data.

        Args:
            edge: An edge in the format (u, v, data), where data contains weight.
        """
        u, v, data = edge
        weight = data.get("weight", 1)
        if weight < 0:
            raise ValueError(
                "Graph contains negative edge weights and not supported by algorithm."
            )
        if dist_to[u] + weight < dist_to[v]:
            dist_to[v] = dist_to[u] + weight
            edge_to[v] = (u, v, data)
            if v in impq.location:
                impq.decrease_priority(v, dist_to[v])
            else:
                impq.enqueue(v, dist_to[v])

    # Main loop of Dijkstra's algorithm
    while not impq.is_empty():
        current_node = impq.dequeue()
        for edge in G.edges(current_node, data=True):
            relax(edge)

    return dist_to, edge_to


def edges_path_to(edge_to, src, target):
    """
    Reconstruct the path from src to target using edge_to.

    Args:
        edge_to: A dictionary of edges leading to each vertex.
        src: The source vertex.
        target: The target vertex.

    Returns:
        path: A list of vertices representing the shortest path from src to target.

    Raises:
        ValueError: If target is unreachable from src.
    """
    if target == src:
        return [src]
    if target not in edge_to:
        raise ValueError(f"Target node {target} is unreachable from source node {src}.")

    path = []
    current = target

    # Reconstruct the path
    while current != src:
        path.append(current)
        current = edge_to[current][0]

    # Add the starting vertex and reverse the path
    path.append(src)
    path.reverse()
    return path
