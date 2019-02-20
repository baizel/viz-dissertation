import json
import string
from collections import namedtuple, deque
from typing import List

Edge = namedtuple('Edge', 'startNodeId, endNodeId, distance')
inf = float('inf')


class UpdateStructure:
    """Should write a class to represent the state of each update function and that
     {
         updates:[
            {
                mapping:int,
                explanation:string,
                options:{},
                data:{},
                edges:{}
            },
            {}
         ]
     }

     """

    def __init__(self):
        self.updateStruct = dict()
        self.updateStruct["updates"] = []

    def addToUpdateQueue(self, codeToLineNumber: int, explanation: string = None, options: dict = None,
                         edges: dict = None,
                         data: dict = None):
        update = {
            "mapping": codeToLineNumber,
            "explanation": explanation,
            "options": options,
            "data": data,
            "edges": edges
        }
        self.updateStruct["updates"].append(update)

    def getUpdates(self):
        return dict(**self.updateStruct)


class PesudoCode:
    def __init__(self):
        self.mapping = UpdateStructure()

    def createVertex(self, Q: list):
        self.mapping.addToUpdateQueue(2, "Create an empty set of vertex Q")
        print(Q)

    def setDistPrevToInf(self, Q: list, distance: dict, prev: dict):
        self.mapping.addToUpdateQueue(5, "Set distance of v to be infinity")
        self.mapping.addToUpdateQueue(6, "Set prev distance of v to be infinity")
        self.mapping.addToUpdateQueue(7, "Add v to the set Q")

        print("Nodes:", Q, "Distance: ", distance, "prev: ", prev)

    def updateDist(self, dist: dict, source: int):
        self.mapping.addToUpdateQueue(9, "Set distance of source to be 0")
        print("Distances: ", dist, "Source:", source)

    def setMinU(self, minVertex):
        self.mapping.addToUpdateQueue(12, "Find the lowest distance and set it to u")
        print("Min: ", minVertex)

    def findAltAndCmp(self, alt, distance, vertex):
        self.mapping.addToUpdateQueue(14, "loop for each neighbor of u")
        self.mapping.addToUpdateQueue(15, "Set alternative dist to the length")
        self.mapping.addToUpdateQueue(16, "check if alt is less than dist")
        print("if {} < {} ".format(alt, distance[vertex]))

    def setDistAndPrevToAlt(self, distance, prev, currentVertex, alt, u):
        self.mapping.addToUpdateQueue(17)
        self.mapping.addToUpdateQueue(18)
        print("dist[{}] = {}, prev[{}]= {}".format(currentVertex, alt, currentVertex, u))

    def removeU(self, currentVertex):
        self.mapping.addToUpdateQueue(20)
        print("remove: ", currentVertex)

    def ret(self, dist, prev):
        self.mapping.addToUpdateQueue(22)
        print(dist, prev)

    def getUpdates(self):
        return dict(**self.mapping.getUpdates())


class Graph:
    def __init__(self, d: dict):
        """
        :param data: Dictionary containing the representation of the node. Uses same structure as http://visjs.org/docs/data/dataset.html
        """
        # Temp data until i get api working
        # data = json.loads(
        #     '{"_options":{},'
        #     '"_data":{"1":{"from":1,"to":3,"id":1,"label":"5","color":{"color":"blue"}},"2":{"from":1,"to":2,"id":2,'
        #     '"label":"12","chosen":true},"3":{"from":2,"to":4,"id":3,"label":"25","chosen":true},"4":{"from":2,"to":5,'
        #     '"id":4,"label":"10","chosen":true}},"length":4,"_fieldId":"id","_type":{},"_subscribers":{"add":[{}],'
        #     '"update":[{}],"remove":[{}]}}')
        data = d['edges']
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
        code = PesudoCode()
        # 1. Mark all nodes unvisited and store them.
        # 2. Set the distance to zero for our initial node
        # and to infinity for other nodes.
        distances = {}
        previousVertices = {}

        code.createVertex([])

        for vertex in self.nodes:
            n = []
            distances[vertex] = inf
            previousVertices[vertex] = None
            n.append(vertex)
            code.setDistPrevToInf(n, distances, previousVertices)

        distances[source] = 0
        code.updateDist(distances, source)

        nodes = self.nodes.copy()
        while nodes:
            # 3. Select the unvisited node with the smallest distance,
            # it's current node now.
            currentVertex = min(nodes, key=lambda vertex: distances[vertex])
            code.setMinU(currentVertex)

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
                code.findAltAndCmp(alternativeRoute, distances, neighbour)
                if alternativeRoute < distances[neighbour]:
                    distances[neighbour] = alternativeRoute
                    previousVertices[neighbour] = currentVertex
                    code.setDistAndPrevToAlt(distances, previousVertices, neighbour, alternativeRoute, currentVertex)

            # 5. Mark the current node as visited
            # and remove it from the unvisited set.
            code.removeU(currentVertex)
            nodes.remove(currentVertex)

        code.ret(distances, previousVertices)
        code.getUpdates()
        return distances, previousVertices, code.getUpdates()
