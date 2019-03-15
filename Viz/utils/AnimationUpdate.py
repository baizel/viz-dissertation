from Viz.pesudo_algorithms.algorithmExporter import Algorithm


class AnimationUpdate:
    """Should write a class to represent the state of each update function and that
     {
         updates:[
            {
                mapping:int,
                explanation:string,
                options:{},
                data:{},
                edges:{}
            },
            {}
         ]
     }

     """

    def __init__(self, algorithmFile):
        self.updateStruct = dict()
        self.updateStruct["updates"] = []
        self.lines = Algorithm(algorithmFile).getJsonAlgo()['lines']

    def addToUpdateQueue(self, codeToLineNumber: int,
                         options: dict = None,
                         edges: list = None,
                         nodes: list = None,
                         data: dict = None):
        update = {
            "mapping": codeToLineNumber,
            "explanation": self.lines[codeToLineNumber].get("exp", ""),
            "options": options,
            "data": data,
            "edges": edges if edges is not None else [],
            "nodes": nodes if nodes is not None else []
        }
        self.updateStruct["updates"].append(update)

    def getUpdates(self):
        return dict(**self.updateStruct)
