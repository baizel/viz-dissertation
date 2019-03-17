from collections import namedtuple
from typing import List

# Edge = namedtuple('Edge', 'startNodeId, endNodeId, distance, edgeId')
from Viz.Graph.DataSet import Edge, Node

INF = float('inf')


class Graph:

    def __init__(self, rawData: dict):
        """
        :param data: Dictionary containing the representation of the node. Uses same structure as http://visjs.org/docs/data/dataset.html
        """
        data = rawData['edges']
        self.edges, self.nodes = Node.fromRaw(rawData)

    def getNode(self, nodeId):
        rt = [i for i in self.nodes if str(i.id) == str(nodeId)]
        return rt[0] if len(rt) > 0 else None
