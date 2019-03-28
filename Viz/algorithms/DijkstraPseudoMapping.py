from Viz.Graph.DataSet import Node, Edge
from Viz.utils.AnimationEngine import AnimationEngine, ExtraData, HighlightEdges
from Viz.utils.context import NEIGHBOUR_NODE_COLOR, SELECTED_NODE_COLOR, CURRENT_NODE_COLOR


class DijkstraPseudoMapping:
    def __init__(self):
        self.animation = AnimationEngine("Dijkstra.txt")
        self.distanceId = "distID"
        self.prevId = "prevID"
        self.QId = "qID"
        self.minUID = "minUID"
        self.neighbourID = "neighbourID"
        self.altAdditionID = "altAdditionID"
        self.cmpCostID = "cmpCostID"
        self.returnDataID = "returnDataID"
        self.displayNames = {
            self.distanceId: "All Distances",
            self.prevId: "Optimal Previous Node",
            self.QId: "Set of all nodes in Q",
            self.minUID: "Node with the smallest distance from source",
            self.neighbourID: "Neighbour of <span class='data {}table'></>".format(self.minUID),  # Not clean but will do to show current node
        }
        self.edgeHighlighting = HighlightEdges()

    def initDistAndPrev(self, dist, prev):
        self.animation.addToUpdateQueue(6)
        self.animation.addToUpdateQueue(7, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance", self.displayNames[self.distanceId]))
        self.animation.addToUpdateQueue(8, data=ExtraData.addSingleTableDataAndGet(self.prevId, prev, "Previous", self.displayNames[self.prevId]))

    def updateDist(self, dist: dict):
        self.animation.addToUpdateQueue(11, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance", self.displayNames))

    def initQ(self, q):
        self.animation.addToUpdateQueue(12, data=ExtraData.addSingleTableDataAndGet(self.QId, q, "Q", self.displayNames[self.QId]))

    def setMinU(self, minVertex):
        nodes = [{"id": minVertex.id, "color": CURRENT_NODE_COLOR, "label": str(minVertex.id)}]
        self.animation.addToUpdateQueue(15, data=ExtraData.addSingleTableDataAndGet(self.minUID, minVertex, "Smallest Node", self.displayNames[self.minUID]), nodes=nodes)

    def removeU(self, q, source: Node):
        self.animation.addToUpdateQueue(16, data=ExtraData.addSingleTableDataAndGet(self.QId, q, "Q", self.displayNames[self.QId]))

        nodes = [{"id": source.id, "color": CURRENT_NODE_COLOR, "label": str(source.id)}]
        neighbour = [i.toNode for i in source.neighbourEdge]
        if len(neighbour) > 0:
            nodes += [{"id": i, "color": NEIGHBOUR_NODE_COLOR, "label": str(i)} for i in neighbour]
        self.animation.addToUpdateQueue(17, data=ExtraData.addSingleTableDataAndGet(self.neighbourID, neighbour, "Neighbour node(s)", self.displayNames[self.neighbourID]), nodes=nodes)

    def findAltAndCmp(self, distance, cost, u, v, previous, dijkSource, graph):
        edge = self.edgeHighlighting.getEdges(distance, previous, u, v, cost, dijkSource, graph)
        self.animation.addToUpdateQueue(18, data=ExtraData.addSingleTableDataAndGet(self.altAdditionID, "{} + {}".format(distance[u], cost)), edges=edge)
        self.animation.addToUpdateQueue(19, data=ExtraData.addSingleTableDataAndGet(self.cmpCostID, "{} < {}".format(distance[u] + cost, distance[v])))

    def setDistAndPrevToAlt(self, dist, prev):
        self.animation.addToUpdateQueue(20, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance", self.displayNames))
        self.animation.addToUpdateQueue(21, data=ExtraData.addSingleTableDataAndGet(self.prevId, prev, "Previous", self.displayNames[self.prevId]))
        self.animation.addToUpdateQueue(22)

    def ret(self, dist, prev):
        self.animation.addToUpdateQueue(23)
        self.animation.addToUpdateQueue(24)
        self.animation.addToUpdateQueue(25, data=ExtraData.addSingleTableDataAndGet(self.returnDataID, "Distance: {}, Previous: {}".format(dist, prev), ""))

    def getUpdates(self):
        return self.animation.getFrames()
