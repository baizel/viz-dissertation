from .DijkstraPseudoMapping import DijkstraPseudoMapping
from .Graph import INF, Graph


class Dijkstra:
    def __init__(self, graph: Graph, source: int):
        assert source in graph.nodes, 'Such source node doesn\'t exist'
        mapping = DijkstraPseudoMapping()
        # 1. Mark all nodes unvisited and store them.
        # 2. Set the distance to zero for our initial node
        # and to infinity for other nodes.
        distances = {}
        previousVertices = {}

        for vertex in graph.nodes:
            distances[vertex] = INF
            previousVertices[vertex] = None
            mapping.initDistAndPrev(distances, previousVertices)

        distances[source] = 0
        mapping.updateDist(distances, source)

        nodes = graph.nodes.copy()
        mapping.initQ(nodes)
        while nodes:
            # 3. Select the unvisited node with the smallest distance,
            # it's current node now.
            currentVertex = min(nodes, key=lambda vertex: distances[vertex])
            mapping.setMinU(currentVertex)
            nodes.remove(currentVertex)
            mapping.removeU(nodes,
                            [n for n, _ in graph.neighbours[currentVertex]])  # only get neighbour not the cost)

            # 4. Find unvisited neighbors for the current node
            # and calculate their distances through the current node.

            for neighbour, cost in graph.neighbours[currentVertex]:
                alternativeRoute = distances[currentVertex] + cost
                # Compare the newly calculated distance to the assigned
                # and save the smaller one.
                mapping.findAltAndCmp(distances[currentVertex], distances[neighbour], cost)
                if alternativeRoute < distances[neighbour]:
                    distances[neighbour] = alternativeRoute
                    previousVertices[neighbour] = currentVertex
                    mapping.setDistAndPrevToAlt(distances, previousVertices)

        mapping.ret(distances, previousVertices)

        self.source = source
        self.distances = distances
        self.previousVertices = previousVertices
        self.animationUpdates = mapping.getUpdates()
