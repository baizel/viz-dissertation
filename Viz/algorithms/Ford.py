import string

from Viz.Graph.Graph import INF, Graph
from Viz.utils.AnimationEngine import AnimationEngine, ExtraData, HighlightEdges
from Viz.utils.context import CURRENT_NODE_COLOR, SELECTED_NODE_COLOR, NEIGHBOUR_NODE_COLOR


class BellmanFordMapping:
    def __init__(self):
        self.animationEngine = AnimationEngine("BellmanFord.txt")
        self.distanceId = "distID"
        self.prevId = "prevID"
        self.uID = "uID"
        self.vID = "vID"
        self.wID = "wID"
        self.innerIfD = "innerIfID"
        self.innerIfDBool = "innerIfIDBool"
        self.outIfDBool = "outIfIDBool"
        self.equalDistID = "equalDistID"
        self.equalPrevID = "equalPrevID"
        self.errCheckID = "errCheckID"
        self.retID = "retID"
        self.errorUID = "errorUID"
        self.edgeHighlighter = HighlightEdges()
        self.displayNames = {
            self.distanceId: "All Distances",
            self.prevId: "Optimal Previous Node",
            self.uID: "Start Node - U",
            self.vID: "End Node - V",
            self.wID: "Distance - W",
        }

    def initDistAndPrev(self, dist, prev):
        self.animationEngine.addToUpdateQueue(6)
        self.animationEngine.addToUpdateQueue(7, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance", self.displayNames[self.distanceId], "Distance"))
        self.animationEngine.addToUpdateQueue(8, data=ExtraData.addSingleTableDataAndGet(self.prevId, prev, "Previous", self.displayNames[self.prevId], "Previous"))

    def firstForLoop(self, dist):
        self.animationEngine.addToUpdateQueue(9)
        self.animationEngine.addToUpdateQueue(10, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance", self.displayNames))
        self.animationEngine.addToUpdateQueue(11)

    def innerLoop(self, u, v, w, distance, graph, sourceNode, previous):
        data = ExtraData(self.uID, "u = {}, v = {}, distanceBetween({},{}) = {}".format(u, v, u, v, w))
        data.addToTable(self.uID, self.displayNames[self.uID], u)
        data.addToTable(self.vID, self.displayNames[self.vID], v)
        data.addToTable(self.wID, self.displayNames[self.wID], w)
        nodes = [{"id": u.id, "color": CURRENT_NODE_COLOR}, {"id": v, "color": NEIGHBOUR_NODE_COLOR}]
        self.animationEngine.addToUpdateQueue(12, data=data, nodes=nodes)
        self.animationEngine.addToUpdateQueue(13, edges=self.edgeHighlighter.getEdges(distance, previous, u, v, w, sourceNode, graph), data=ExtraData.addSingleTableDataAndGet(
            self.innerIfD, "{} + {} < {} = {}".format(distance[u], w, distance[v], distance[u] + w < distance[v])))
        self.animationEngine.addToUpdateQueue(14, data=ExtraData.addSingleTableDataAndGet(self.innerIfDBool, str(distance[u] + w < distance[v])))

    def ifStatement(self, u, v, w, distances, previous):
        data13 = ExtraData(self.equalDistID, "distance[{}] = {} + {}".format(v, distances[u], w))
        data13.addToUpdateDataQueue(self.distanceId, distances, isShownOnScreen=False, inlineExp="Distance")

        data14 = ExtraData(self.equalPrevID, "previous[{}] = {}".format(v, u))
        data14.addToUpdateDataQueue(self.prevId, previous, isShownOnScreen=False, inlineExp="Previous")

        self.animationEngine.addToUpdateQueue(15, data=data13)
        self.animationEngine.addToUpdateQueue(16, data=data14)

    def secondForLoop(self):
        self.animationEngine.addToUpdateQueue(17)
        self.animationEngine.addToUpdateQueue(18)
        self.animationEngine.addToUpdateQueue(19)
        self.animationEngine.addToUpdateQueue(20)

    def innerIf(self, u, v, w, distance, previous, graph, source):
        data = ExtraData(self.errorUID, "u = {}, v = {}, distanceBetween({},{}) = {}".format(u, v, u, v, w))
        self.animationEngine.addToUpdateQueue(20, data=data)
        self.animationEngine.addToUpdateQueue(21, edges=self.edgeHighlighter.getEdges(distance, previous, u, v, w, source, graph), data=ExtraData.addSingleTableDataAndGet(
            self.errCheckID, "{} + {} ({}) < {}".format(distance[u], w, distance[u] + w, distance[v])))

        self.animationEngine.addToUpdateQueue(22, data=ExtraData.addSingleTableDataAndGet(self.outIfDBool, (str((distance[u] + w) < distance[v]))))

    def err(self):
        self.animationEngine.addToUpdateQueue(23)

    def ret(self, dist, prev):
        self.animationEngine.addToUpdateQueue(24)
        self.animationEngine.addToUpdateQueue(25)
        data = ExtraData(self.distanceId, dist, isShownOnScreen=False, inlineExp="Distance")
        data.addToUpdateDataQueue(self.prevId, prev, isShownOnScreen=False, inlineExp="Previous")
        data.addToUpdateDataQueue(self.retID, "Dist {}, Prev {}".format(dist, prev), isShownOnScreen=True)
        self.animationEngine.addToUpdateQueue(26, data=data)

    def getUpdates(self):
        return self.animationEngine.getFrames()


class BellmanFord:
    def __init__(self, graph: Graph, source: string):
        source = graph.getNode(source)
        assert source is not None, 'Such source node doesn\'t exist'
        mapping = BellmanFordMapping()

        distances = {}
        previousVertices = {}

        for vertex in graph.nodes:
            distances[vertex] = INF
            previousVertices[vertex] = None
            mapping.initDistAndPrev(distances, previousVertices)

        distances[source] = 0
        mapping.firstForLoop(distances)
        for _ in range(len(graph.nodes.copy()) - 1):
            for edges in graph.edges.copy():
                u = graph.getNode(edges.fromNode)
                v = graph.getNode(edges.toNode)
                w = edges.distance
                mapping.innerLoop(u, v, w, distances, graph, source, previousVertices)
                if distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    previousVertices[v] = u
                    mapping.ifStatement(u, v, w, distances, previousVertices)

        mapping.secondForLoop()
        for edges in graph.edges.copy():
            u = graph.getNode(edges.fromNode)
            v = graph.getNode(edges.toNode)
            w = edges.distance

            mapping.innerIf(u, v, w, distances, previousVertices, graph, source)
            if distances[u] + w < distances[v]:
                print("Error negative weight cycles")
                mapping.err()
                self.animationUpdates = mapping.getUpdates()
                return

        mapping.ret(distances, previousVertices)
        self.animationUpdates = mapping.getUpdates()
