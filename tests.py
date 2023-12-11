import unittest
from main import Graph
from collections import defaultdict


class TestGraphAlgorithms(unittest.TestCase):
    def test_graph_construction(self):
        graph = Graph(5)
        self.assertEqual(graph.V, 5)
        self.assertEqual(graph.graph, defaultdict(list))

    def test_add_edge(self):
        graph = Graph(5)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        self.assertEqual(graph.graph, {0: [1], 1: [0, 2], 2: [1]})

    def test_dfs_articulation_points(self):
        graph = Graph(5)
        edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
        for edge in edges:
            graph.add_edge(*edge)

        num_points, points, elapsed_time = graph.find_articulation_points_dfs()

        self.assertEqual(num_points, 2)
        self.assertEqual(set(points), {1, 3})
        self.assertGreater(elapsed_time, 0)

    def test_tarjan_articulation_points(self):
        graph = Graph(5)
        edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
        for edge in edges:
            graph.add_edge(*edge)

        num_points, points, elapsed_time = graph.find_articulation_points_tarjan()

        self.assertEqual(num_points, 2)
        self.assertEqual(set(points), {1, 3})
        self.assertGreater(elapsed_time, 0)


if __name__ == '__main__':
    unittest.main()