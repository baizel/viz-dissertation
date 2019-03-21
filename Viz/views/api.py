import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse

from Viz.Graph.DataSet import Node, Edge
from Viz.Graph.Dijkstra import Dijkstra
from Viz.Graph.Graph import Graph

context: dict = dict()


def ser(obj):
    if isinstance(obj, Node):
        return obj.id
    if isinstance(obj, Edge):
        return obj.toNode
    return obj.__dict__


def index(request: WSGIRequest, algorithm, source) -> HttpResponse:
    ret = {}
    network = json.loads(request.GET['network'])
    graph = Graph(network)

    if algorithm == "dijkstra":
        ret = Dijkstra(graph, source).animationUpdates

    return JsonResponse(json.loads(json.dumps(ret, default=ser)))
