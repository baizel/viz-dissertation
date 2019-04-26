import random
from typing import List

from Viz.Graph.DataSet import Edge, Node

INF = float('inf')


class Graph:

    def __init__(self, rawData: dict):
        """
        :param data: Dictionary containing the representation of the node. Uses same structure as http://visjs.org/docs/data/dataset.html
        """
        self.__rawData = rawData

        self.edges: List[Edge]
        self.nodes: List[Node]
        self.edges, self.nodes = self.__fromRaw(rawData)

    def __fromRaw(self, data) -> (List['Edge'], List['Node']):
        edges = []
        nodes = []
        for n in data["nodes"]["_data"]:
            nodeData = data["nodes"]["_data"][n]
            node = Node(nodeData["id"], nodeData["label"], nodeData.get("color"))
            nodes.append(node)

        for e in data["edges"]["_data"]:
            edgeData = data["edges"]["_data"][e]
            edge = Edge(edgeData["id"], edgeData["from"], edgeData["to"], int(edgeData["distance"]), edgeData["label"])
            edges.append(edge)
            fromNode = [i for i in nodes if i.id == edge.fromNode][0]  # Edge must exist with a from node
            fromNode.neighbourEdge.append(edge)
        return edges, nodes

    def getRawData(self):
        return self.__rawData

    def getNode(self, nodeId):
        rt = [i for i in self.nodes if str(i.id) == str(nodeId)]
        return rt[0] if len(rt) > 0 else None

    def getEdge(self, fromNodeId, toNodeId):
        rt = [i for i in self.edges if str(i.toNode) == str(toNodeId) and str(fromNodeId) == str(i.fromNode)]
        return rt[0] if len(rt) > 0 else None

    def getJavaScriptData(self):
        return {"nodes": self.nodes, "edges": self.edges}

    @classmethod
    def generateRandomGraph(cls, numberOfNodes, numberOfEdges=None, isNegativeEdges=False):
        lowerBound = (int(isNegativeEdges) * -50)  # Will be 1 or -50
        if numberOfEdges is None:
            numberOfEdges = numberOfNodes * 2  # Just try to add much edges as it can for now, maybe add an api end point?
        nodes = {}
        edges = {}
        for i in range(1, numberOfNodes + 1):
            n = {"id": i, "label": str(i)}
            nodes[str(i)] = n
        for i in range(1, numberOfEdges):
            dist = random.randrange(lowerBound, 50) + 1  # +1 to prevent 0 as distance for positive edges
            fromNode = random.randrange(1, numberOfNodes + 1)
            toNode = random.randrange(1, numberOfNodes + 1)
            e = Edge(i, fromNode, toNode, dist, str(dist))

            if edges not in e and toNode != fromNode:  # Weird order of 'edges not in e' because code when executed needs to be '!e.__contains__(edges)'  instead of edges.__contains__(e)
                edges[e.id] = e.getJson()
        rawData = {"nodes": {"_data": nodes}, "edges": {"_data": edges}}
        return Graph(rawData)
