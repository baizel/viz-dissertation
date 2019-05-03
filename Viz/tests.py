import json

from django.test import TestCase

from Viz.Graph.DataSet import Node
from Viz.Graph.Graph import Graph
from Viz.algorithms.Dijkstra import Dijkstra
from Viz.algorithms.Floyd import FloydWarshall
from Viz.algorithms.Ford import BellmanFord
from Viz.utils.context import NodeEdgeSerializer

inf = float("inf")
raw = json.loads(
    '{"nodes":{"_options":{},"_data":{"1":{"id":1,"label":"1"},"2":{"id":2,'
    '"label":"2"},"3":{"id":3,"label":"3"},"4":{"id":4,"label":"4"},"5":{"id":5,'
    '"label":"5"},"6":{"id":6,"label":"6"},"7":{"id":7,"label":"7"}},'
    '"length":7,"_fieldId":"id","_type":{},"_subscribers":{"add":[{}],"update":[{}],'
    '"remove":[{}]}},"edges":{"_options":{},"_data":{"1":{"id":1,"from":1,'
    '"to":7,"label":"48","distance":48},"2":{"id":2,"from":4,"to":7,"label":"26",'
    '"distance":26},"3":{"id":3,"from":3,"to":6,"label":"12","distance":12},'
    '"4":{"id":4,"from":7,"to":4,"label":"27","distance":27},'
    '"5":{"id":5,"from":1,"to":3,"label":"25","distance":25},"6":{"id":6,"'
    'from":6,"to":4,"label":"14","distance":14},"8":'
    '{"id":8,"from":7,"to":3,"label":"4","distance":4},"9":{"id":9,"from":5,"'
    'to":6,"label":"44","distance":44},"11":{"id":11,"from":1,"to":2,"label":'
    '"38","distance":38},"13":{"id":13,'
    '"from":3,"to":7,"label":"21","distance":21}},"length":10,"_fieldId":"id",'
    '"_type":{},"_subscribers":{"add":[{}],"update":[{}],"remove":[{}]}}}')
graph = Graph(raw)
ans = {
    1: {1: 0, 2: 38, 3: 25, 4: 51, 5: inf, 6: 37, 7: 46},
    2: {1: inf, 2: 0, 3: inf, 4: inf, 5: inf, 6: inf, 7: inf},
    3: {1: inf, 2: inf, 3: 0, 4: 26, 5: inf, 6: 12, 7: 21},
    4: {1: inf, 2: inf, 3: 30, 4: 0, 5: inf, 6: 42, 7: 26},
    5: {1: inf, 2: inf, 3: 88, 4: 58, 5: 0, 6: 44, 7: 84},
    6: {1: inf, 2: inf, 3: 44, 4: 14, 5: inf, 6: 0, 7: 40},
    7: {1: inf, 2: inf, 3: 4, 4: 27, 5: inf, 6: 16, 7: 0}
}


class DijkstraTestCase(TestCase):
    def test_all_distances(self):
        for source in ans.keys():
            for nodes, distance in Dijkstra(graph, source).distances.items():
                self.assertEqual(ans[source][nodes.id], distance)


#
class BellmanFordTestCase(TestCase):
    def test_all_distances(self):
        for source in ans.keys():
            for nodes, distance in BellmanFord(graph, source).distances.items():
                self.assertEqual(ans[source][nodes.id], distance)


class FloydWarshallTestCase(TestCase):
    def test_all_distances(self):
        for source, distanceRow in FloydWarshall(graph).distances.items():
            for node, distance in distanceRow.items():
                self.assertEqual(ans[source.id][node.id], distance)
