import json

from Viz.Graph import Graph
from Viz.Graph.DataSet import Edge
from Viz.Graph.Graph import INF


class Mapping:
    # TODO: implement this?
    pass


class FloydWarshall:
    @staticmethod
    def __initDistances(nodes):
        columns = {}
        for i in nodes:
            row = {}
            for j in nodes:
                row[j] = INF
            columns[i] = row
        return columns

    def __init__(self, graph: Graph):
        distance = self.__initDistances(graph.nodes)

        edges: Edge
        for edges in graph.edges.copy():
            u = graph.getNode(edges.fromNode)
            v = graph.getNode(edges.toNode)
            distance[u][v] = edges.distance

        for node in graph.nodes.copy():
            distance[node][node] = 0

        for i in graph.nodes.copy():
            for j in graph.nodes.copy():
                for k in graph.nodes.copy():
                    alt = distance[j][i] + distance[i][k]
                    if distance[j][k] > alt:
                        distance[j][k] = alt

    @staticmethod
    def makeHTMLtable(distance):
        # TODO: turn this into a html string
        for k, v in distance.items():
            print("<b>" + str(k) + "</b>", end=" ")
            for key, val in v.items():
                print(val, end=" ")
            print("")
