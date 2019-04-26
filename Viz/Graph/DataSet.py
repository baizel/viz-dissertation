import string
from typing import List


class Options:
    def __init__(self):
        pass


class Node:
    def __init__(self, nodeId: string, label: string, color: string, edges: List['Edge'] = None, options: Options = None):
        self.__id: string = nodeId
        self.__neighbourEdge = edges if edges is not None else []
        self.__label = label
        self.__color = color
        self.__options = options

    def getJson(self):
        return {"id": self.__id, "label": self.__label}

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

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return self.__str__()


class Edge:
    def __init__(self, id, fromNode: string, toNode: string, distance: int, label: string, options: Options = None):
        self.fromNode: string = fromNode
        self.toNode: string = toNode
        self.distance: int = distance
        self.label: string = label
        self.options: Options = options
        self.id: string = id

    def __str__(self):
        return "from {} to {} dist {} label {}".format(self.fromNode, self.toNode, self.distance, self.label)

    def __contains__(self, item):
        ret = False
        if isinstance(item, dict):
            for j in item:
                i = item[j]
                ret += i.get("from", None) == self.fromNode and i.get("to", None) == self.toNode
            return ret
        return item in self

    def getJson(self):
        """ Only used for to send edge data to create random graph """
        return {"id": self.id, "from": self.fromNode, "to": self.toNode, "label": str(self.distance), "distance": self.distance}

    def __repr__(self):
        return self.__str__()
