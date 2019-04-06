from Viz.Graph.DataSet import Node, Edge
from Viz.utils.AnimationEngine import AnimationEngine, ExtraData, HighlightEdges
from Viz.utils.context import NEIGHBOUR_NODE_COLOR, SELECTED_NODE_COLOR, CURRENT_NODE_COLOR


class DijkstraPseudoMapping:
    distanceId = "distID"
    prevId = "prevID"
    QId = "qID"
    minUID = "minUID"
    neighbourID = "neighbourID"
    altAdditionID = "altAdditionID"
    cmpCostID = "cmpCostID"
    returnDataID = "returnDataID"

    def __init__(self):
        self.animationEngine = AnimationEngine("Dijkstra.txt")
        self.displayNames = {
            self.distanceId: "All Distances",
            self.prevId: "Optimal Previous Node",
            self.QId: "Set of all nodes in Q",
            self.minUID: "Node with the smallest distance from source",
            self.neighbourID: "Neighbour of <span class='data {}table'></>".format(self.minUID),  # Not clean but will do to show current node
        }
        self.edgeHighlighting = HighlightEdges()

    def initDistAndPrev(self, dist, prev):
        self.animationEngine.addToUpdateQueue(6)
        self.animationEngine.addToUpdateQueue(7, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance", self.displayNames[self.distanceId]))
        self.animationEngine.addToUpdateQueue(8, data=ExtraData.addSingleTableDataAndGet(self.prevId, prev, "Previous", self.displayNames[self.prevId]))

    def updateDist(self, dist: dict):
        self.animationEngine.addToUpdateQueue(11, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance", self.displayNames))

    def initQ(self, q):
        self.animationEngine.addToUpdateQueue(12, data=ExtraData.addSingleTableDataAndGet(self.QId, q, "Q", self.displayNames[self.QId]))

    def setMinU(self, minVertex):
        nodes = [{"id": minVertex.id, "color": CURRENT_NODE_COLOR, "label": str(minVertex.id)}]
        self.animationEngine.addToUpdateQueue(15, data=ExtraData.addSingleTableDataAndGet(self.minUID, minVertex, "Smallest Node", self.displayNames[self.minUID]), nodes=nodes)

    def removeU(self, q, source: Node):
        self.animationEngine.addToUpdateQueue(16, data=ExtraData.addSingleTableDataAndGet(self.QId, q, "Q", self.displayNames[self.QId]))

        nodes = [{"id": source.id, "color": CURRENT_NODE_COLOR, "label": str(source.id)}]
        neighbour = [i.toNode for i in source.neighbourEdge]
        if len(neighbour) > 0:
            nodes += [{"id": i, "color": NEIGHBOUR_NODE_COLOR, "label": str(i)} for i in neighbour]
        self.animationEngine.addToUpdateQueue(17, data=ExtraData.addSingleTableDataAndGet(self.neighbourID, neighbour, "Neighbour node(s)", self.displayNames[self.neighbourID]), nodes=nodes)

    def findAltAndCmp(self, distance, cost, u, v, previous, dijkSource, graph):
        edge = self.edgeHighlighting.getEdges(distance, previous, u, v, cost, dijkSource, graph)
        self.animationEngine.addToUpdateQueue(18, data=ExtraData.addSingleTableDataAndGet(self.altAdditionID, "{} + {}".format(distance[u], cost)), edges=edge)
        self.animationEngine.addToUpdateQueue(19, data=ExtraData.addSingleTableDataAndGet(self.cmpCostID, "{} < {}".format(distance[u] + cost, distance[v])))

    def setDistAndPrevToAlt(self, dist, prev):
        self.animationEngine.addToUpdateQueue(20, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance", self.displayNames))
        self.animationEngine.addToUpdateQueue(21, data=ExtraData.addSingleTableDataAndGet(self.prevId, prev, "Previous", self.displayNames[self.prevId]))
        self.animationEngine.addToUpdateQueue(22)

    def ret(self, dist, prev):
        self.animationEngine.addToUpdateQueue(23)
        self.animationEngine.addToUpdateQueue(24)
        self.animationEngine.addToUpdateQueue(25, data=ExtraData.addSingleTableDataAndGet(self.returnDataID, "Distance: {}, Previous: {}".format(dist, prev), ""))

    def getUpdates(self):
        return self.animationEngine.getFrames()
