import string

from Viz.Graph.Graph import INF, Graph


class BellmanFord:
    def __init__(self, graph: Graph, source: string):
        source = graph.getNode(source)
        assert source is not None, 'Such source node doesn\'t exist'

        distances = {}
        previousVertices = {}

        for vertex in graph.nodes:
            distances[vertex] = INF
            previousVertices[vertex] = None

        distances[source] = 0

        for _ in range(len(graph.nodes.copy()) - 1):
            for edges in graph.edges.copy():
                u = graph.getNode(edges.fromNode)
                v = graph.getNode(edges.toNode)
                w = edges.distance
                if distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w

        for edges in graph.edges.copy():
            u = graph.getNode(edges.fromNode)
            v = graph.getNode(edges.toNode)
            w = edges.distance
            if distances[u] + w < distances[v]:
                print("Error negative weight cycles")
                return
