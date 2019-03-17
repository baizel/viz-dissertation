import string

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
                         options: dict = None,
                         edges: list = None,
                         nodes: list = None,
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
