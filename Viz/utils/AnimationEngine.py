import string

from Viz.Graph.DataSet import Node, Edge
from Viz.algorithms.pesudo_algorithms.algorithmExporter import PseudoAlgorithm
from Viz.utils.context import SELECTED_NODE_COLOR, Singleton


class HighlightEdges(metaclass=Singleton):
    animationEdgeIDCounter = 0

    def getEdges(self, distance, previous, u, v, w, source, graph):
        self.animationEdgeIDCounter += 1
        edge = [{"id": "animation" + str(self.animationEdgeIDCounter), "from": u.id, "to": v.id, "label": "{} + {} ({}) < {}".format(
            distance[u], w, distance[u] + w, distance[v]), "color": {"color": SELECTED_NODE_COLOR}}]

        base = u
        pathNodes = [] if base is None else [u]
        while base is not None and base != source.id:
            base = previous[base]
            if base is not None:
                cycle = previous[base]
                if cycle is not None and base == previous[cycle]:
                    # a cycle in the system
                    break
                pathNodes.append(base)
        pathEdges = []
        if len(pathNodes) > 1:
            for i in range(0, len(pathNodes) - 1):
                edgeId = graph.getEdge(pathNodes[i + 1], pathNodes[i]).id
                e = {"id": edgeId, "color": {"color": SELECTED_NODE_COLOR}, "isNew": False}
                pathEdges.append(e)

        edge += pathEdges
        return edge


class ExtraData:
    def __init__(self, classId, value, inlineExp=None, isShownOnScreen=True):
        """
        Whatever used as the initial value will be used to shown as the inline data IF and ONLY IF inlineExp is not None. Provide empty string if wanting to be shown but not pre-append anything
        when wanting to update more data without showing inline statement use addToUpdateDataQueue()
        :param classId: Class Id used to track of all data in html
        :param value: value of data
        :param inlineExp: String in english to append before showing the data inline, can be NOne in which case will not show anything before
        """
        self.__data = {"tableData": [], "updateData": [{"classID": classId, "rawData": ExtraData.__sanitise(value), "inlineExp": inlineExp, "isShownOnScreen": isShownOnScreen}]}

    def addToTable(self, classId, tableName, value):
        """
        Use this method when wanting to update the table of variables
        :param classId:  Class Id used to track of all data in html
        :param tableName: writing shown in the 'name' column of the table, can be a short description
        :param value: value of the data
        :return: NOen
        """
        self.__data["tableData"].append({"classID": classId, "tableExp": tableName, "rawData": ExtraData.__sanitise(value)})

    def addToUpdateDataQueue(self, classId, value, inlineExp=None, isShownOnScreen=False):
        """
        Used to silently update data through out the document
        :param inlineExp:
        :param classId: Class Id used to track of all data in html
        :param value: value of data
        :return:
        """
        self.__data["updateData"].append({"classID": classId, "rawData": ExtraData.__sanitise(value), "inlineExp": inlineExp, "isShownOnScreen": isShownOnScreen})

    def getData(self):
        return self.__data

    @staticmethod
    def __sanitise(data):
        if isinstance(data, dict):
            return "{}".format(data)
        if isinstance(data, set):
            return "{}" if len(data) == 0 else data
        if isinstance(data, Node):
            return str(data.id)
        if isinstance(data, Edge):
            return "Error, Type 'Edge' Not Expected!"
        return str(data)

    @staticmethod
    def addSingleTableDataAndGet(classId, value, inlineExp=None, tableName=None, isShownOnScreen=True):
        a = ExtraData(classId, value, inlineExp, isShownOnScreen=isShownOnScreen)
        if tableName is not None:
            a.addToTable(classId, tableName, value)
        return a


class AnimationEngine:
    """Class to represent the state of each Frame that has the following schemea
     {
         updates:[
            {
                mapping:int,
                explanation:string,
                options:{},
                data:[],
                edges:[]
            },
            ...
         ]
     }

     """

    def __init__(self, algorithmFile):
        self.frames = dict()
        self.frames["updates"] = []
        self.pesudoAlgorithm = PseudoAlgorithm(algorithmFile)
        self.lines = self.pesudoAlgorithm.getJsonAlgo()['lines']
        self.nodeOrder = []
        self.edgeOrder = []

    def addToFrames(self, codeToLineNumber: int,
                    options: dict = None,  # Same as vis.js options used for update
                    edges: list = None,  # Same as vis.js edges used for update
                    nodes: list = None,  # Same as vis.js nodes used for update
                    data: ExtraData = None,
                    overrideExplanation: string = None):
        if nodes is not None and len(nodes) > 0:
            self.nodeOrder.append({codeToLineNumber: nodes})
        if edges is not None and len(edges) > 0:
            self.edgeOrder.append({codeToLineNumber: edges})
        update = {
            "mapping": codeToLineNumber,
            "explanation": self.lines[codeToLineNumber].get("exp", "") if overrideExplanation is None else overrideExplanation,
            "options": options,
            "data": data if data is None else data.getData(),
            "edges": edges if edges is not None else [],
            "nodes": nodes if nodes is not None else []
        }
        self.frames["updates"].append(update)

    def getFrames(self):
        return dict(**self.frames)
