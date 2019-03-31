import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse

from Viz.Graph.DataSet import Node, Edge
from Viz.algorithms.Dijkstra import Dijkstra
from Viz.Graph.Graph import Graph
from Viz.algorithms.Floyd import FloydWarshall
from Viz.algorithms.Ford import BellmanFord

context: dict = dict()


def ser(obj):
    if isinstance(obj, Node):
        return obj.id
    if isinstance(obj, Edge):
        return obj.toNode
    return obj.__dict__


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
        ret = BellmanFord(graph,source).animationUpdates
    elif algorithm == "floyd":
        ret = FloydWarshall(graph).ree

    return JsonResponse(json.loads(json.dumps(ret, default=ser)))
