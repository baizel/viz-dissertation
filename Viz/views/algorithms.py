import json

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render_to_response
from django.http import HttpResponse

from Viz.Graph.Graph import Graph
from Viz.pesudo_algorithms.algorithmExporter import Algorithm

from Viz.utils.context import Context

context: dict = dict()


def index(request: WSGIRequest, algorithm) -> HttpResponse:
    cntx = Context()
    res = cntx.getContext()
    if algorithm == "dijkstra":
        algo = Algorithm("Dijkstra.txt")
        res["jsonAlgo"] = json.dumps(algo.getJsonAlgo())
        res["pageTitle"] = "Dijkstra Algorithm"
        res["apiAlgo"] = "'dijkstra'"
    else:
        return render_to_response("algorithm_not_supported.html")

    return render_to_response("algorithm_base.html", res)
