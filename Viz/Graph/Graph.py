import json
from collections import namedtuple, deque

Edge = namedtuple('Edge', 'startNodeId, endNodeId, distance')
inf = float('inf')


class PesudoCode:
    def __int__(self):
        self.mapping = {}

    def createVertex(self, Q: list):
        print(Q)

    def setDistPrevToInf(self, Q: list, distance: dict, prev: dict):
        print("Nodes:", Q, "Distance: ", distance, "prev: ", prev)

    def updateDist(self, dist: dict, source: int):
        print("Distances: ", dist, "Source:", source)

    def setMinU(self, minVertex):
        print("Min: ", minVertex)

    def findAltAndCmp(self, alt, distance, vertex):
        print("if {} < {} ".format(alt,distance[vertex]))

    def setDistAndPrevToAlt(self, distance, prev, currentVertex, alt, u):
        print("dist[{}] = {}, prev[{}]= {}".format(currentVertex, alt, currentVertex, u))

    def removeU(self, currentVertex):
        print("remove: ", currentVertex)

    def ret(self, dist, prev):
        print(dist, prev)


class Graph:
    def __init__(self, data: dict):
        """
        :param data: Dictionary containing the representation of the node. Uses same structure as http://visjs.org/docs/data/dataset.html
        """
        # Temp data until
        data = json.loads(
            '{"_options":{},'
            '"_data":{"1":{"from":1,"to":3,"id":1,"label":"5","color":{"color":"blue"}},"2":{"from":1,"to":2,"id":2,'
            '"label":"12","chosen":true},"3":{"from":2,"to":4,"id":3,"label":"25","chosen":true},"4":{"from":2,"to":5,'
            '"id":4,"label":"10","chosen":true}},"length":4,"_fieldId":"id","_type":{},"_subscribers":{"add":[{}],'
            '"update":[{}],"remove":[{}]}}')

        self.edges = [Edge(data["_data"][edges]['from'], data["_data"][edges]['to'], int(data["_data"][edges]['label']))
                      for edges in data["_data"]]
        print(self.edges)

    @property
    def nodes(self):
        return set(
            sum(([edge.startNodeId, edge.endNodeId] for edge in self.edges), [])
        )

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.nodes}
        for edge in self.edges:
            neighbours[edge.startNodeId].add((edge.endNodeId, edge.distance))
        return neighbours

    def dijkstra(self, source):
        assert source in self.nodes, 'Such source node doesn\'t exist'
        pesudo = PesudoCode()
        # 1. Mark all nodes unvisited and store them.
        # 2. Set the distance to zero for our initial node
        # and to infinity for other nodes.
        distances = {}
        previousVertices = {}

        pesudo.createVertex([])

        for vertex in self.nodes:
            n = []
            distances[vertex] = inf
            previousVertices[vertex] = None
            n.append(vertex)
            pesudo.setDistPrevToInf(n, distances, previousVertices)

        distances[source] = 0
        pesudo.updateDist(distances, source)

        nodes = self.nodes.copy()
        while nodes:
            # 3. Select the unvisited node with the smallest distance,
            # it's current node now.
            currentVertex = min(nodes, key=lambda vertex: distances[vertex])
            pesudo.setMinU(currentVertex)

            # 6. Stop, if the smallest distance
            # among the unvisited nodes is infinity.
            if distances[currentVertex] == inf:
                break

            # 4. Find unvisited neighbors for the current node
            # and calculate their distances through the current node.
            for neighbour, cost in self.neighbours[currentVertex]:
                alternativeRoute = distances[currentVertex] + cost
                # Compare the newly calculated distance to the assigned
                # and save the smaller one.
                pesudo.findAltAndCmp(alternativeRoute, distances, neighbour)
                if alternativeRoute < distances[neighbour]:
                    distances[neighbour] = alternativeRoute
                    previousVertices[neighbour] = currentVertex
                    pesudo.setDistAndPrevToAlt(distances, previousVertices, neighbour, alternativeRoute, currentVertex)

            # 5. Mark the current node as visited
            # and remove it from the unvisited set.
            pesudo.removeU(currentVertex)
            nodes.remove(currentVertex)

        pesudo.ret(distances, previousVertices)
        return distances, previousVertices
