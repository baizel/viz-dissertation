import json

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse

from Viz.Graph.Graph import Graph
from Viz.pesudo_algorithms.algorithmExporter import Algorithm

from Viz.utils.context import Context

context: dict = dict()


def index(request: WSGIRequest) -> HttpResponse:
    network = json.loads(request.GET['network'])
    source = json.loads(request.GET['source'])
    g = Graph(network)
    distances, _, updates = g.dijkstra(source)
    return JsonResponse({"updates": updates})
