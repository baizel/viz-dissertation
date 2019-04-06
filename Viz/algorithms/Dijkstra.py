import string

from Viz.algorithms.DijkstraPseudoMapping import DijkstraPseudoMapping
from Viz.Graph.Graph import INF, Graph


class Dijkstra:
    def __init__(self, graph: Graph, source: string):
        source = graph.getNode(source)
        assert source is not None, 'Such source node doesn\'t exist'
        self.__mapping = DijkstraPseudoMapping()

        # 1. Mark all nodes unvisited and store them.
        # 2. Set the distance to zero for our initial node
        # and to infinity for other nodes.
        distances = {}
        previousVertices = {}

        for vertex in graph.nodes:
            distances[vertex] = INF
            previousVertices[vertex] = None
            self.__mapping.initDistAndPrev(distances, previousVertices)

        distances[source] = 0
        self.__mapping.updateDist(distances)

        nodes = graph.nodes.copy()
        self.__mapping.initQ(nodes)
        while nodes:
            # 3. Select the unvisited node with the smallest distance,
            # it's current node now.
            currentVertex = min(nodes, key=lambda v: distances[v])
            self.__mapping.setMinU(currentVertex)
            nodes.remove(currentVertex)
            self.__mapping.removeU(nodes, currentVertex)  # only get neighbour not the cost)

            # 4. Find unvisited neighbors for the current node
            # and calculate their distances through the current node.

            for edge in currentVertex.neighbourEdge:
                neighbour = graph.getNode(edge.toNode)
                cost = edge.distance

                alternativeRoute = distances[currentVertex] + cost
                # Compare the newly calculated distance to the assigned
                # and save the smaller one.
                self.__mapping.findAltAndCmp(distances, cost, currentVertex, neighbour, previousVertices, source, graph)
                if alternativeRoute < distances[neighbour]:
                    distances[neighbour] = alternativeRoute
                    previousVertices[neighbour] = currentVertex
                    self.__mapping.setDistAndPrevToAlt(distances, previousVertices)

        self.__mapping.ret(distances, previousVertices)

        self.source = source
        self.distances = distances
        self.previousVertices = previousVertices
        self.animationUpdates = self.__mapping.getUpdates()


    def getAnimationEngine(self):
        return self.__mapping.animationEngine
