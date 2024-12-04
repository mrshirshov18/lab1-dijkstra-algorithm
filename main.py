import networkx as nx
from dijkstra.shortest_sp import dijkstra_sp, edges_path_to


def main():
    # Create a directed graph with weights
    G = nx.DiGraph()
    edges = [
        (0, 1, 4),  # Edge from 0 to 1 with weight 4
        (0, 2, 1),  # Edge from 0 to 2 with weight 1
        (2, 1, 2),  # Edge from 2 to 1 with weight 2
        (1, 3, 1),  # Edge from 1 to 3 with weight 1
        (2, 3, 5),  # Edge from 2 to 3 with weight 5
        (3, 4, 3),  # Edge from 3 to 4 with weight 3
    ]
    G.add_weighted_edges_from(edges)

    # Source vertex and target vertex
    src = 0
    target = 4

    # Run Dijkstra's algorithm
    dist_to, edge_to = dijkstra_sp(G, src)

    # Print shortest distances to all nodes
    print(f"Shortest distances from vertex {src}:")
    for node, dist in dist_to.items():
        print(f"  To vertex {node}: {dist}")

    # Reconstruct the path to the target vertex
    try:
        path = edges_path_to(edge_to, src, target)
        print(f"\nShortest path from {src} to {target}: {path}")
    except ValueError as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
