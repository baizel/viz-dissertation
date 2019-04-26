import string

from Viz.algorithms.DijkstraPseudoMapping import DijkstraPseudoMapping
from Viz.Graph.Graph import INF, Graph


class Dijkstra:
    def __init__(self, graph: Graph, source: string):
        self.__graph = Graph
        source = graph.getNode(source)
        assert source is not None, 'Such source node doesn\'t exist'
        self.__mapping = DijkstraPseudoMapping()

        distances = {}
        previousVertices = {}

        for vertex in graph.nodes:
            distances[vertex] = INF
            previousVertices[vertex] = None
            self.__mapping.initDistAndPrev(distances, previousVertices)

        distances[source] = 0
        self.__mapping.updateDist(distances)

        Q = graph.nodes.copy()
        self.__mapping.initQ(Q)
        while Q:
            u = min(Q, key=lambda i: distances[i])
            self.__mapping.setMinU(u)
            Q.remove(u)
            self.__mapping.removeU(Q, u)

            for edge in u.neighbourEdge:
                v = graph.getNode(edge.toNode)
                alternativeRoute = distances[u] + edge.distance
                self.__mapping.findAltAndCmp(distances, edge.distance, u, v, previousVertices, source, graph)
                if alternativeRoute < distances[v]:
                    distances[v] = alternativeRoute
                    previousVertices[v] = u
                    self.__mapping.setDistAndPrevToAlt(distances, previousVertices)

        self.distances = distances
        self.previousVertices = previousVertices

        self.__mapping.ret(distances, previousVertices)
        self.source = source
        self.animationUpdates = self.__mapping.getFrames()


    def getAnimationEngine(self):
        return self.__mapping.animationEngine
