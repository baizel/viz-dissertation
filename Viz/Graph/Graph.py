from collections import namedtuple

Edge = namedtuple('Edge', 'startNodeId, endNodeId, distance')
INF = float('inf')


class Graph:
    def __init__(self, d: dict):
        """
        :param data: Dictionary containing the representation of the node. Uses same structure as http://visjs.org/docs/data/dataset.html
        """
        # Temp data until i get api working
        # data = json.loads(
        #     '{"_options":{},'
        #     '"_data":{"1":{"from":1,"to":3,"id":1,"label":"5","color":{"color":"blue"}},"2":{"from":1,"to":2,"id":2,'
        #     '"label":"12","chosen":true},"3":{"from":2,"to":4,"id":3,"label":"25","chosen":true},"4":{"from":2,"to":5,'
        #     '"id":4,"label":"10","chosen":true}},"length":4,"_fieldId":"id","_type":{},"_subscribers":{"add":[{}],'
        #     '"update":[{}],"remove":[{}]}}')
        data = d['edges']
        self.edges = [Edge(data["_data"][edges]['from'], data["_data"][edges]['to'], int(data["_data"][edges]['label']))
                      for edges in data["_data"]]
        print(self.edges)

    @property
    def nodes(self):
        return set(
            sum(([edge.startNodeId, edge.endNodeId] for edge in self.edges), [])
        )

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.nodes}
        for edge in self.edges:
            neighbours[edge.startNodeId].add((edge.endNodeId, edge.distance))
        return neighbours
