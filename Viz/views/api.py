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
        return obj.getJson()
    if isinstance(obj, Edge):
        return obj.getJson()
    return obj.__dict__


def randomGraph(request: WSGIRequest, numberOfNodes=8):
    ret = Graph.generateRandomGraph(numberOfNodes).getJavaScriptData()
    err = JsonResponse(json.loads(json.dumps(ret, default=ser)))
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
