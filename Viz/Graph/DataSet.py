import string
from typing import List


class Options:
    def __init__(self):
        pass


class Node:
    def __init__(self, nodeId: string, label: string, color: string, edges: List['Edge'] = None, options: Options = None):
        self.__id = nodeId
        self.__neighbourEdge = edges if edges is not None else []
        self.__label = label
        self.__color = color
        self.__options = options

    @property
    def id(self):
        return self.__id

    @property
    def neighbourEdge(self):
        return self.__neighbourEdge

    @property
    def label(self):
        return self.__label

    @property
    def color(self):
        return self.__color

    @property
    def options(self):
        return self.__options

    @classmethod
    def fromRaw(cls, data: dict) -> (List['Edge'], List['Node']):
        edges = []
        nodes = []
        for n in data["nodes"]["_data"]:
            nodeData = data["nodes"]["_data"][n]
            node = Node(nodeData["id"], nodeData["label"], nodeData.get("color"))
            nodes.append(node)

        for e in data["edges"]["_data"]:
            edgeData = data["edges"]["_data"][e]
            edge = Edge(edgeData["id"],edgeData["from"], edgeData["to"], int(edgeData["distance"]), edgeData["label"])
            edges.append(edge)
            fromNode = [i for i in nodes if i.id == edge.fromNode][0]  # Edge must exist with a from node
            fromNode.neighbourEdge.append(edge)
        return edges, nodes

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return self.__str__()


class Edge:
    def __init__(self, id,fromNode: string, toNode: string, distance: int, label: string, options: Options = None):
        self.fromNode = fromNode
        self.toNode = toNode
        self.distance = distance
        self.label = label
        self.options = options
        self.id = id
    def __str__(self):
        return "from {} to {} dist {} label {}".format(self.fromNode, self.toNode, self.distance, self.label)

    #
    # @classmethod
    # def fromRaw(cls, data: dict) -> List['Edge']:
    #     rt = []
    #     for edges in data["edges"]["_data"]:
    #         edgeData = data["edges"]["_data"][edges]
    #         fromNode = data.get("nodes").get("_data").get(str(edgeData.get("from")))
    #         toNode = data.get("nodes").get("_data").get(str(edgeData.get("to")))
    #         edge = Edge(Node(fromNode.get("id"), fromNode.get("label")), Node(toNode.get("id"), toNode.get("label")), int(edgeData.get("distance")), edgeData.get("label"))
    #         rt.append(edge)
    #     return rt
    def __repr__(self):
        return self.__str__()