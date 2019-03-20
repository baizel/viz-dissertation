import json
import string

from Viz.Graph.DataSet import Node, Edge
from Viz.pesudo_algorithms.algorithmExporter import Algorithm


class AnimationUpdate:
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
        self.lines = Algorithm(algorithmFile).getJsonAlgo()['lines']

    def addToUpdateQueue(self, codeToLineNumber: int,
                         options: dict = None,  # Same as vis.js options used for update
                         edges: list = None,  # Same as vis.js edges used for update
                         nodes: list = None,  # Same as vis.js nodes used for update
                         data: dict = None,
                         overrideExplanation: string = None):
        update = {
            "mapping": codeToLineNumber,
            "explanation": self.lines[codeToLineNumber].get("exp", "") if overrideExplanation is None else overrideExplanation,
            "options": options,
            "data": data,
            "edges": edges if edges is not None else [],
            "nodes": nodes if nodes is not None else []
        }
        self.frames["updates"].append(update)

    def getFrames(self):
        return dict(**self.frames)

    @staticmethod
    def getLineData(classId, rawData, inlineExp=None, tableName=None):
        return {"classID": classId, "rawData": AnimationUpdate.__sanitise(rawData), "inlineExp": inlineExp, "tableExp": tableName}

    @staticmethod
    def __sanitise(data):
        if (isinstance(data, dict)):
            return "{}".format(data)
        if isinstance(data, set):
            return "{}" if len(data) == 0 else data
        if isinstance(data, Node):
            return str(data.id)
        if isinstance(data, Edge):
            return "Error, Type 'Edge' Not Expected!"
        return str(data)
