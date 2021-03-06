from Viz.Graph.DataSet import Node, Edge
from Viz.utils.AnimationEngine import AnimationEngine, ExtraData, HighlightEdges
from Viz.utils.context import NEIGHBOUR_NODE_COLOR, CURRENT_NODE_COLOR


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
            self.neighbourID: "Neighbour of <span class='data {}table'></>".format(self.minUID),
        }
        self.edgeHighlighting = HighlightEdges()

    def initDistAndPrev(self, dist: dict, prev: dict):
        datal7 = ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance", self.displayNames[self.distanceId])
        datal8 = ExtraData.addSingleTableDataAndGet(self.prevId, prev, "Previous", self.displayNames[self.prevId])
        self.animationEngine.addToFrames(6)
        self.animationEngine.addToFrames(7, data=datal7)
        self.animationEngine.addToFrames(8, data=datal8)

    def updateDist(self, dist: dict):
        self.animationEngine.addToFrames(11, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance",
                                                                                     self.displayNames))

    def initQ(self, q):
        self.animationEngine.addToFrames(12, data=ExtraData.addSingleTableDataAndGet(self.QId, q, "Q",
                                                                                     self.displayNames[self.QId]))

    def setMinU(self, minVertex):
        nodes = [{"id": minVertex.id, "color": CURRENT_NODE_COLOR, "label": str(minVertex.id)}]
        data = ExtraData.addSingleTableDataAndGet(self.minUID, minVertex, "Smallest Node", self.displayNames[self.minUID])
        self.animationEngine.addToFrames(15, data=data, nodes=nodes)

    def removeU(self, q, source: Node):
        self.animationEngine.addToFrames(16, data=ExtraData.addSingleTableDataAndGet(self.QId, q, "Q",
                                                                                     self.displayNames[self.QId]))

        nodes = [{"id": source.id, "color": CURRENT_NODE_COLOR, "label": str(source.id)}]
        neighbour = [i.toNode for i in source.neighbourEdge]
        if len(neighbour) > 0:
            nodes += [{"id": i, "color": NEIGHBOUR_NODE_COLOR, "label": str(i)} for i in neighbour]
        extraData = ExtraData.addSingleTableDataAndGet(
            self.neighbourID,
            neighbour,
            "Neighbour node(s)",
            self.displayNames[self.neighbourID]
        )
        self.animationEngine.addToFrames(17, data=extraData, nodes=nodes)

    def findAltAndCmp(self, distance, cost, u, v, previous, dijkSource, graph):
        edge = self.edgeHighlighting.getEdges(distance, previous, u, v, cost, dijkSource, graph)
        self.animationEngine.addToFrames(18, data=ExtraData.addSingleTableDataAndGet(
            self.altAdditionID, "{} + {}".format(distance[u], cost)
        ), edges=edge)
        self.animationEngine.addToFrames(19, data=ExtraData.addSingleTableDataAndGet(
            self.cmpCostID, "{} < {}".format(distance[u] + cost, distance[v])
        ))

    def setDistAndPrevToAlt(self, dist, prev):
        self.animationEngine.addToFrames(20, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance",
                                                                                     self.displayNames)
                                         )
        self.animationEngine.addToFrames(21, data=ExtraData.addSingleTableDataAndGet(self.prevId, prev, "Previous",
                                                                                     self.displayNames[self.prevId])
                                         )
        self.animationEngine.addToFrames(22)

    def ret(self, dist, prev):
        self.animationEngine.addToFrames(23)
        self.animationEngine.addToFrames(24)
        self.animationEngine.addToFrames(25, data=ExtraData.addSingleTableDataAndGet(self.returnDataID,
                                                                                     "Distance: {}, Previous: {}".format(dist, prev), ""))

    def getFrames(self):
        return self.animationEngine.getFrames()
