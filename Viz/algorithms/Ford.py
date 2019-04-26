import string

from Viz.Graph.Graph import INF, Graph
from Viz.utils.AnimationEngine import AnimationEngine, ExtraData, HighlightEdges
from Viz.utils.context import CURRENT_NODE_COLOR, SELECTED_NODE_COLOR, NEIGHBOUR_NODE_COLOR


class FordPseudoMapping:
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
        self.animationEngine.addToFrames(6)
        self.animationEngine.addToFrames(7, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance", self.displayNames[self.distanceId], "Distance"))
        self.animationEngine.addToFrames(8, data=ExtraData.addSingleTableDataAndGet(self.prevId, prev, "Previous", self.displayNames[self.prevId], "Previous"))

    def firstForLoop(self, dist):
        self.animationEngine.addToFrames(9)
        self.animationEngine.addToFrames(10, data=ExtraData.addSingleTableDataAndGet(self.distanceId, dist, "Distance", self.displayNames))
        self.animationEngine.addToFrames(11)

    def innerLoop(self, u, v, w, distance, graph, sourceNode, previous):
        data = ExtraData(self.uID, "u = {}, v = {}, distanceBetween({},{}) = {}".format(u, v, u, v, w))
        data.addToTable(self.uID, self.displayNames[self.uID], u)
        data.addToTable(self.vID, self.displayNames[self.vID], v)
        data.addToTable(self.wID, self.displayNames[self.wID], w)
        nodes = [{"id": u.id, "color": CURRENT_NODE_COLOR}, {"id": v.id, "color": NEIGHBOUR_NODE_COLOR}]
        self.animationEngine.addToFrames(12, data=data, nodes=nodes)
        self.animationEngine.addToFrames(13, edges=self.edgeHighlighter.getEdges(distance, previous, u, v, w, sourceNode, graph), data=ExtraData.addSingleTableDataAndGet(
            self.innerIfD, "{} + {} < {} = {}".format(distance[u], w, distance[v], distance[u] + w < distance[v])))
        self.animationEngine.addToFrames(14, data=ExtraData.addSingleTableDataAndGet(self.innerIfDBool, str(distance[u] + w < distance[v])))

    def ifStatement(self, u, v, w, distances, previous):
        data13 = ExtraData(self.equalDistID, "distance[{}] = {} + {}".format(v, distances[u], w))
        data13.addToUpdateDataQueue(self.distanceId, distances, isShownOnScreen=False, inlineExp="Distance")

        data14 = ExtraData(self.equalPrevID, "previous[{}] = {}".format(v, u))
        data14.addToUpdateDataQueue(self.prevId, previous, isShownOnScreen=False, inlineExp="Previous")

        self.animationEngine.addToFrames(15, data=data13)
        self.animationEngine.addToFrames(16, data=data14)

    def secondForLoop(self):
        self.animationEngine.addToFrames(17)
        self.animationEngine.addToFrames(18)
        self.animationEngine.addToFrames(19)
        self.animationEngine.addToFrames(20)

    def innerIf(self, u, v, w, distance, previous, graph, source):
        data = ExtraData(self.errorUID, "u = {}, v = {}, distanceBetween({},{}) = {}".format(u, v, u, v, w))
        self.animationEngine.addToFrames(20, data=data)
        self.animationEngine.addToFrames(21, edges=self.edgeHighlighter.getEdges(distance, previous, u, v, w, source, graph), data=ExtraData.addSingleTableDataAndGet(
            self.errCheckID, "{} + {} ({}) < {}".format(distance[u], w, distance[u] + w, distance[v])))

        self.animationEngine.addToFrames(22, data=ExtraData.addSingleTableDataAndGet(self.outIfDBool, (str((distance[u] + w) < distance[v]))))

    def err(self):
        self.animationEngine.addToFrames(23)

    def ret(self, dist, prev):
        self.animationEngine.addToFrames(24)
        self.animationEngine.addToFrames(25)
        data = ExtraData(self.distanceId, dist, isShownOnScreen=False, inlineExp="Distance")
        data.addToUpdateDataQueue(self.prevId, prev, isShownOnScreen=False, inlineExp="Previous")
        data.addToUpdateDataQueue(self.retID, "Dist {}, OI OI OI Prev {}".format(dist, prev), isShownOnScreen=False)
        self.animationEngine.addToFrames(26, data=data)

    def getFrames(self):
        return self.animationEngine.getFrames()


class BellmanFord:
    def __init__(self, graph: Graph, source: string):
        self.__graph = Graph
        source = graph.getNode(source)
        assert source is not None, 'Such source node doesn\'t exist'
        self.__mapping = FordPseudoMapping()

        distances = {}
        previousVertices = {}

        for vertex in graph.nodes:
            distances[vertex] = INF
            previousVertices[vertex] = None
            self.__mapping.initDistAndPrev(distances, previousVertices)

        distances[source] = 0
        self.__mapping.firstForLoop(distances)
        for _ in range(len(graph.nodes) - 1):
            for edges in graph.edges.copy():
                u = graph.getNode(edges.fromNode)
                v = graph.getNode(edges.toNode)
                w = edges.distance
                self.__mapping.innerLoop(u, v, w, distances, graph, source, previousVertices)
                alternative = distances[u] + w
                if alternative < distances[v]:
                    distances[v] = alternative
                    previousVertices[v] = u
                    self.__mapping.ifStatement(u, v, w, distances, previousVertices)

        self.__mapping.secondForLoop()
        for edges in graph.edges.copy():
            u = graph.getNode(edges.fromNode)
            v = graph.getNode(edges.toNode)
            w = edges.distance

            self.__mapping.innerIf(u, v, w, distances, previousVertices, graph, source)
            if distances[u] + w < distances[v]:
                print("Error negative weight cycles")
                self.__mapping.err()
                self.animationUpdates = self.__mapping.getFrames()
                return

        self.distances = distances
        self.previous = previousVertices
        self.__mapping.ret(distances, previousVertices)

        self.animationUpdates = self.__mapping.getFrames()

    def getAnimationEngine(self):
        return self.__mapping.animationEngine
