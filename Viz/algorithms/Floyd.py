import json

from Viz.Graph import Graph
from Viz.Graph.DataSet import Edge
from Viz.Graph.Graph import INF
from Viz.utils.AnimationEngine import AnimationEngine, ExtraData
from Viz.utils.context import CURRENT_NODE_COLOR_HTML, SELECTED_NODE_COLOR_HTML, NEIGHBOUR_NODE_COLOR_HTML, CURRENT_NODE_COLOR, SELECTED_NODE_COLOR, NEIGHBOUR_NODE_COLOR


class Mapping:
    def __init__(self):
        self.__animationEngine = AnimationEngine("FloydWarshall.txt")
        self.tableMatrixID = "TableMatrixID"
        self.tableMatrixLabel = "Distance Matrix"
        self.forLoopI = "iForLoopId"
        self.forLoopJ = "jForLoopId"
        self.forLoopK = "kForLoopId"

    def setToInf(self, htmlTable):
        self.__animationEngine.addToUpdateQueue(5, data=ExtraData.addSingleTableDataAndGet(self.tableMatrixID, htmlTable, tableName=self.tableMatrixLabel, isShownOnScreen=False))

    def setDistances(self, htmlTable):
        self.__animationEngine.addToUpdateQueue(7)
        self.__animationEngine.addToUpdateQueue(8, data=ExtraData.addSingleTableDataAndGet(self.tableMatrixID, htmlTable, tableName=self.tableMatrixLabel, isShownOnScreen=False))

    def setToZero(self, htmlTable):
        self.__animationEngine.addToUpdateQueue(10)
        self.__animationEngine.addToUpdateQueue(11, data=ExtraData.addSingleTableDataAndGet(self.tableMatrixID, htmlTable, tableName=self.tableMatrixLabel, isShownOnScreen=False))

    def iLoop(self, i):
        nodes = [{"id": i.id, "color": NEIGHBOUR_NODE_COLOR}]
        self.__animationEngine.addToUpdateQueue(13, data=ExtraData.addSingleTableDataAndGet(self.forLoopI, i, inlineExp="i ="), nodes=nodes)

    def jLoop(self, j):
        nodes = [{"id": j.id, "color": SELECTED_NODE_COLOR}]
        self.__animationEngine.addToUpdateQueue(14, data=ExtraData.addSingleTableDataAndGet(self.forLoopJ, j, inlineExp="j ="), nodes=nodes)

    def kLoop(self, i, j, k, distance, htmlTable):
        nodes = [{"id": k.id, "color": CURRENT_NODE_COLOR}, {"id": j.id, "color": SELECTED_NODE_COLOR}, {"id": i.id, "color": NEIGHBOUR_NODE_COLOR}]
        data = ExtraData(self.forLoopK, k, inlineExp="k =", isShownOnScreen=True)
        data.addToTable(self.tableMatrixID, self.tableMatrixLabel, htmlTable)
        exp = self.__createExp(i, j, k, distance)
        self.__animationEngine.addToUpdateQueue(15, data=data, nodes=nodes, overrideExplanation=exp)
        self.__animationEngine.addToUpdateQueue(16,overrideExplanation=exp)

    def assignDistance(self, i, j, k, distance, htmlTable):
        exp = self.__createExp(i, j, k, distance)
        self.__animationEngine.addToUpdateQueue(17, data=ExtraData.addSingleTableDataAndGet(self.tableMatrixID, htmlTable, tableName=self.tableMatrixLabel, isShownOnScreen=False),
                                                overrideExplanation=exp)
        self.__animationEngine.addToUpdateQueue(18, overrideExplanation=exp)

    def ret(self):
        self.__animationEngine.addToUpdateQueue(19)
        self.__animationEngine.addToUpdateQueue(20)
        self.__animationEngine.addToUpdateQueue(21)
        self.__animationEngine.addToUpdateQueue(22)
        self.__animationEngine.addToUpdateQueue(23)

    def __createExp(self, i, j, k, distance):
        exp = "The distance from node {}<code>(j)</code> to node <code>{}(i)</code> is <code>{} <span class='{}'>(distance[j][i])</span></code></br>".format(j, i, distance[j][i], SELECTED_NODE_COLOR_HTML)
        exp += "The distance from node <code>{}(i)</code> to node <code>{}(k)</code> is <code>{}  <span class='{}'>(distance[i][k])</span></code></br>".format(i, k, distance[i][k], NEIGHBOUR_NODE_COLOR_HTML)
        exp += "Therefore, <span class='{}'><code>distance[j][k]</code></span> can be <span class='{}'><code>distance[i][k]</code></span> + <span class='{}'><code>distance[j][i]</code></span>" \
               " if the old value is bigger than the new one</br>" \
            .format(CURRENT_NODE_COLOR_HTML, NEIGHBOUR_NODE_COLOR_HTML, SELECTED_NODE_COLOR_HTML)
        exp += "<code>><span class='{}'>distance[{}][{}]</span> > <span class='{}'>distance[{}][{}]</span> +  <span class='{}'>distance[{}][{}]</span></code></br>".format(CURRENT_NODE_COLOR_HTML, j, k,
                                                                                                                                                                           SELECTED_NODE_COLOR_HTML, j, i,
                                                                                                                                                                           NEIGHBOUR_NODE_COLOR_HTML, i, k)

        exp += "><code><span class='{}'>{}</span> > <span class='{}'>{}</span> + <span class='{}'>{}</span></code></br>".format(CURRENT_NODE_COLOR_HTML, distance[j][k], SELECTED_NODE_COLOR_HTML, distance[j][i],
                                                                                                                                NEIGHBOUR_NODE_COLOR_HTML, distance[i][k])
        return exp

    def getFrames(self):
        return self.__animationEngine.getFrames()


class FloydWarshall:
    @staticmethod
    def __initDistances(nodes):
        columns = {}
        for i in nodes:
            row = {}
            for j in nodes:
                row[j] = INF
            columns[i] = row
        return columns

    def __init__(self, graph: Graph):
        m = Mapping()
        distance = self.__initDistances(graph.nodes)
        m.setToInf(self.makeHTMLtable(distance))

        edges: Edge
        for edges in graph.edges.copy():
            u = graph.getNode(edges.fromNode)
            v = graph.getNode(edges.toNode)
            distance[u][v] = edges.distance
            m.setDistances(self.makeHTMLtable(distance, None, u, v))

        for node in graph.nodes.copy():
            distance[node][node] = 0
            m.setToZero(self.makeHTMLtable(distance, node, node))

        for i in graph.nodes.copy():
            m.iLoop(i)
            for j in graph.nodes.copy():
                m.jLoop(j)
                for k in graph.nodes.copy():
                    m.kLoop(i, j, k, distance, self.makeHTMLtable(distance, i, j, k))
                    alt = distance[j][i] + distance[i][k]
                    if distance[j][k] > alt:
                        distance[j][k] = alt
                        m.assignDistance(i, j, k, distance, self.makeHTMLtable(distance, i, j, k))
        m.ret()
        self.ree = m.getFrames()

    @staticmethod
    def makeHTMLtable(distance, i=None, j=None, k=None):
        # TODO: turn this into a html string
        table = "<table class = 'striped centered'> " \
                "<tr> " \
                "<td> Nodes </td>" \
                "{}" \
                "</tr>"
        topRowNodes = ""
        for nodes, listOfNodes in distance.items():
            topRowNodes += "<td><b>{}</b></td>".format(str(nodes))
            row = "<tr> " \
                  "<td><b>" + str(nodes) + "</b> </td>"
            for node, weight in listOfNodes.items():
                color = ""
                if nodes == j:
                    if node == k:
                        color = CURRENT_NODE_COLOR_HTML
                    elif node == i:
                        color = SELECTED_NODE_COLOR_HTML
                elif nodes == i and node == k:
                    color = NEIGHBOUR_NODE_COLOR_HTML
                r = "<td class='{}'>".format(color) + str(weight) + "</td>"
                row += r
            row += "</tr>"
            table += row
        table += "</table>"
        table = table.format(topRowNodes)
        return table
