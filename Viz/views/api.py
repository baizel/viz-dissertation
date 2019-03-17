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


def index(request: WSGIRequest) -> HttpResponse:
    network = json.loads(request.GET['network'])
    source = json.loads(request.GET['source'])
    g = Graph(network)
    algo = Dijkstra(g, source)
    print(json.dumps(algo.animationUpdates,indent=2,default=ser))
    return JsonResponse({"updates": json.dumps(algo.animationUpdates, default=ser)})
