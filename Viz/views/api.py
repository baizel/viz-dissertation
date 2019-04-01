import json
import random

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse

from Viz.Graph.DataSet import Node, Edge
from Viz.algorithms.Dijkstra import Dijkstra
from Viz.Graph.Graph import Graph
from Viz.algorithms.Floyd import FloydWarshall
from Viz.algorithms.Ford import BellmanFord

context: dict = dict()


class EdgeClass:
    def __init__(self, fromNode, toNode, distance):
        self.fromNode = fromNode
        self.toNode = toNode
        self.distance = distance

    def getEdge(self):
        return {"from": self.fromNode, "to": self.toNode, "label": str(self.distance), "distance": self.distance}


def ser(obj):
    if isinstance(obj, Node):
        return obj.id
    if isinstance(obj, EdgeClass):
        return obj.toNode
    return obj.__dict__


def randomGraph(request: WSGIRequest, numberOfNodes=8):
    nodes = []
    edges = []
    for i in range(1, numberOfNodes + 1):
        n = {"id": i, "label": str(i)}
        nodes.append(n)
    for i in range(1, numberOfNodes * 2):  # Just try to add much edges as it can maybe add an api end point
        dist = random.randrange(1, 50)
        fromNode = random.randrange(1, numberOfNodes + 1)
        toNode = random.randrange(1, numberOfNodes + 1)

        e = Edge(None, fromNode, toNode, dist, str(dist))
        if edges not in e and toNode != fromNode:  # Weird order of 'edges not in e' because code when executed needs to be '!e.__contains__(edges)'  instead of edges.__contains__(e)
            edges.append(e.getJson())
    err = JsonResponse({"nodes": nodes, "edges": edges})
    err.status_code = 200
    return err


def index(request: WSGIRequest, algorithm, source=None) -> HttpResponse:
    ret = {"updates": []}
    net = request.GET.get('network')
    if net is None:
        err = JsonResponse({"Error": "No network provided"})
        err.status_code = 404
        return err

    network = json.loads(net)
    graph = Graph(network)

    if algorithm != "floyd":
        if source is None:
            err = JsonResponse({"Error": "No source for algorithm provided"})
            err.status_code = 404
            return err
    if algorithm == "dijkstra":
        ret = Dijkstra(graph, source).animationUpdates
    elif algorithm == "ford":
        ret = BellmanFord(graph, source).animationUpdates
    elif algorithm == "floyd":
        ret = FloydWarshall(graph).ree

    return JsonResponse(json.loads(json.dumps(ret, default=ser)))
