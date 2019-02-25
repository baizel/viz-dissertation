import json
import string
from collections import namedtuple, deque
from typing import List

from Viz.pesudo_algorithms.algorithmExporter import Algorithm

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
        self.lines = Algorithm("Dijkstra.txt").getJsonAlgo()['lines']

    def addToUpdateQueue(self, codeToLineNumber: int,
                         options: dict = None,
                         edges: dict = None,
                         data: dict = None):
        update = {
            "mapping": codeToLineNumber,
            "explanation": self.lines[codeToLineNumber].get("exp", ""),
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
        self.distanceId = "distID"
        self.prevId = "prevID"
        self.QId = "qID"
        self.minUID = "minUID"
        self.neighbourID = "neighbourID"
        self.altAdditionID = "altAdditionID"
        self.cmpCostID = "cmpCostID"
        self.returnDataID = "returnDataID"

    def InitDistAndPrev(self, dist, prev):
        self.mapping.addToUpdateQueue(6)
        # {lineData:{id:data,id:data }
        self.mapping.addToUpdateQueue(7, data={"lineData": [self.distanceId, "distance: {}".format(dist)]})
        self.mapping.addToUpdateQueue(8, data={"lineData": [self.prevId, "previous: {}".format(prev)]})

    def updateDist(self, dist: dict, source: int):
        self.mapping.addToUpdateQueue(11, data={"lineData": [self.distanceId, "distance: {}".format(dist)]})

    def initQ(self, q):
        self.mapping.addToUpdateQueue(12, data={"lineData": [self.QId, "Q: {}".format(q)]})

    def setMinU(self, minVertex):
        self.mapping.addToUpdateQueue(15, data={"lineData": [self.minUID, "Min U: {}".format(minVertex)]})

    def removeU(self, q):
        self.mapping.addToUpdateQueue(16, data={"lineData": [self.QId, "Q: {}".format(q)]})

    def findAltAndCmp(self, uDistance, vDistance, cost, neighbour):
        self.mapping.addToUpdateQueue(17, data={"lineData": [self.neighbourID, "neighbour: {}".format(neighbour)]})
        self.mapping.addToUpdateQueue(18, data={"lineData": [self.altAdditionID, "{} + {}".format(uDistance, cost)]})
        self.mapping.addToUpdateQueue(19, data={
            "lineData": [self.cmpCostID, "{} < {}".format(uDistance + cost, vDistance)]})  # Alt = uDist+cost

    def setDistAndPrevToAlt(self, distance, prev):
        self.mapping.addToUpdateQueue(20, data={"lineData": [self.distanceId, "distance: {}".format(distance)]})
        self.mapping.addToUpdateQueue(21, data={"lineData": [self.prevId, "previous: {}".format(prev)]})
        self.mapping.addToUpdateQueue(22)

    def ret(self, dist, prev):
        self.mapping.addToUpdateQueue(23)
        self.mapping.addToUpdateQueue(24)
        self.mapping.addToUpdateQueue(25, data={
            "lineData": [self.returnDataID, "Distance: {}, Previous: {}".format(dist, prev)]})

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

        for vertex in self.nodes:
            distances[vertex] = inf
            previousVertices[vertex] = None
            code.InitDistAndPrev(distances, previousVertices)

        distances[source] = 0
        code.updateDist(distances, source)

        nodes = self.nodes.copy()
        code.initQ(nodes)
        while nodes:
            # 3. Select the unvisited node with the smallest distance,
            # it's current node now.
            currentVertex = min(nodes, key=lambda vertex: distances[vertex])
            code.setMinU(currentVertex)
            nodes.remove(currentVertex)
            code.removeU(nodes)

            if distances[currentVertex] == inf:
                break

            # 4. Find unvisited neighbors for the current node
            # and calculate their distances through the current node.
            for neighbour, cost in self.neighbours[currentVertex]:
                alternativeRoute = distances[currentVertex] + cost
                # Compare the newly calculated distance to the assigned
                # and save the smaller one.
                code.findAltAndCmp(distances[currentVertex], distances[neighbour], cost,
                                   [n for n, _ in self.neighbours[currentVertex]]) # only get neighbour not the cost
                if alternativeRoute < distances[neighbour]:
                    distances[neighbour] = alternativeRoute
                    previousVertices[neighbour] = currentVertex
                    code.setDistAndPrevToAlt(distances, previousVertices)

        code.ret(distances, previousVertices)
        code.getUpdates()
        return distances, previousVertices, code.getUpdates()
