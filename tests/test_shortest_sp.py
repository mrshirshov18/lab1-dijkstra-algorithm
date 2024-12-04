import unittest
import networkx as nx
from dijkstra.shortest_sp import dijkstra_sp, edges_path_to


class TestDijkstraSP(unittest.TestCase):
    def setUp(self):
        # Common graphs for multiple tests
        self.simple_graph = nx.DiGraph()
        self.simple_graph.add_weighted_edges_from(
            [
                (0, 1, 2),
                (1, 2, 3),
                (0, 2, 4),
            ]
        )

        self.negative_weight_graph = nx.DiGraph()
        self.negative_weight_graph.add_weighted_edges_from(
            [
                (0, 1, -1),
                (1, 2, 2),
            ]
        )

        self.unreachable_graph = nx.DiGraph()
        self.unreachable_graph.add_weighted_edges_from(
            [
                (0, 1, 1),
                (1, 2, 1),
                # Node 3 is unreachable
            ]
        )

        self.cycle_graph = nx.DiGraph()
        self.cycle_graph.add_weighted_edges_from(
            [
                (0, 1, 1),
                (1, 2, 1),
                (2, 0, 1),  # Cycle back to 0
            ]
        )

        self.multiple_paths_graph = nx.DiGraph()
        self.multiple_paths_graph.add_weighted_edges_from(
            [
                (0, 1, 1),
                (0, 2, 5),
                (1, 2, 1),
                (1, 3, 2),
                (2, 3, 1),
                (3, 4, 1),
            ]
        )

    def test_simple_graph(self):
        dist_to, edge_to = dijkstra_sp(self.simple_graph, 0)
        self.assertEqual(dist_to[2], 4)
        path = edges_path_to(edge_to, 0, 2)
        self.assertEqual(path, [0, 2])

    def test_negative_weight_graph(self):
        with self.assertRaises(ValueError) as context:
            dijkstra_sp(self.negative_weight_graph, 0)
        self.assertIn("negative edge weights", str(context.exception))

    def test_unreachable_node(self):
        dist_to, edge_to = dijkstra_sp(self.unreachable_graph, 0)
        self.assertEqual(dist_to[2], 2)
        self.assertEqual(dist_to.get(3, float("inf")), float("inf"))
        with self.assertRaises(ValueError) as context:
            edges_path_to(edge_to, 0, 3)
        self.assertIn("unreachable", str(context.exception))

    def test_cycle_graph(self):
        dist_to, edge_to = dijkstra_sp(self.cycle_graph, 0)
        self.assertEqual(dist_to[2], 2)
        path = edges_path_to(edge_to, 0, 2)
        self.assertEqual(path, [0, 1, 2])

    def test_multiple_paths_graph(self):
        dist_to, edge_to = dijkstra_sp(self.multiple_paths_graph, 0)
        self.assertEqual(dist_to[4], 4)
        path = edges_path_to(edge_to, 0, 4)
        expected_paths = [[0, 1, 2, 3, 4], [0, 1, 3, 4]]
        self.assertIn(path, expected_paths)

    def test_self_loop(self):
        self_loop_graph = nx.DiGraph()
        self_loop_graph.add_weighted_edges_from(
            [
                (0, 0, 0),
                (0, 1, 1),
            ]
        )
        dist_to, edge_to = dijkstra_sp(self_loop_graph, 0)
        self.assertEqual(dist_to[1], 1)
        path = edges_path_to(edge_to, 0, 1)
        self.assertEqual(path, [0, 1])

    def test_disconnected_graph(self):
        disconnected_graph = nx.DiGraph()
        disconnected_graph.add_weighted_edges_from(
            [
                (0, 1, 1),
                (2, 3, 1),
            ]
        )
        dist_to, edge_to = dijkstra_sp(disconnected_graph, 0)
        self.assertEqual(dist_to[0], 0)
        self.assertEqual(dist_to[1], 1)
        self.assertEqual(dist_to.get(2, float("inf")), float("inf"))
        self.assertEqual(dist_to.get(3, float("inf")), float("inf"))
        with self.assertRaises(ValueError):
            edges_path_to(edge_to, 0, 2)

    def test_zero_weight_edges(self):
        zero_weight_graph = nx.DiGraph()
        zero_weight_graph.add_weighted_edges_from(
            [
                (0, 1, 0),
                (1, 2, 0),
                (0, 2, 1),
            ]
        )
        dist_to, edge_to = dijkstra_sp(zero_weight_graph, 0)
        self.assertEqual(dist_to[2], 0)
        path = edges_path_to(edge_to, 0, 2)
        self.assertEqual(path, [0, 1, 2])

    def test_same_source_and_target(self):
        dist_to, edge_to = dijkstra_sp(self.simple_graph, 0)
        path = edges_path_to(edge_to, 0, 0)
        self.assertEqual(path, [0])

    def test_nonexistent_source(self):
        with self.assertRaises(ValueError):
            dijkstra_sp(self.simple_graph, 99)

    def test_no_edges_graph(self):
        no_edges_graph = nx.DiGraph()
        no_edges_graph.add_node(0)
        dist_to, edge_to = dijkstra_sp(no_edges_graph, 0)
        self.assertEqual(dist_to[0], 0)
        path = edges_path_to(edge_to, 0, 0)
        self.assertEqual(path, [0])

    def test_graph_with_multiple_edge_weights(self):
        multi_weight_graph = nx.DiGraph()
        multi_weight_graph.add_edge(0, 1, weight=5)
        multi_weight_graph.add_edge(0, 1, weight=3)
        dist_to, edge_to = dijkstra_sp(multi_weight_graph, 0)
        self.assertEqual(dist_to[1], 3)
        path = edges_path_to(edge_to, 0, 1)
        self.assertEqual(path, [0, 1])

    def test_graph_with_missing_weights(self):
        default_weight_graph = nx.DiGraph()
        default_weight_graph.add_edge(0, 1)  # No weight specified
        default_weight_graph.add_edge(1, 2)  # No weight specified
        dist_to, edge_to = dijkstra_sp(default_weight_graph, 0)
        self.assertEqual(dist_to[2], 2)
        path = edges_path_to(edge_to, 0, 2)
        self.assertEqual(path, [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
