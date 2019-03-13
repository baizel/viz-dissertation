import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse

from Viz.Graph.Dijkstra import Dijkstra
from Viz.Graph.Graph import Graph


context: dict = dict()


def index(request: WSGIRequest) -> HttpResponse:
    network = json.loads(request.GET['network'])
    source = json.loads(request.GET['source'])
    g = Graph(network)
    algo = Dijkstra(g,source)

    return JsonResponse({"updates": algo.animationUpdates})
