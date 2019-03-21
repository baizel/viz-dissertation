import json

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render_to_response
from django.http import HttpResponse

from Viz.algorithms.pesudo_algorithms.algorithmExporter import PesudoAlgorithm
from Viz.utils.context import Context

context: dict = dict()


def index(request: WSGIRequest, algorithm) -> HttpResponse:
    cntx = Context()
    res = cntx.getContext()
    algo = None
    if algorithm == "dijkstra":
        algo = PesudoAlgorithm("Dijkstra.txt")
        res["jsonAlgo"] = json.dumps(algo.getJsonAlgo())
        res["pageTitle"] = "Dijkstra Algorithm"
        res["apiAlgo"] = "'dijkstra'"
    elif algorithm == "floyd":
        algo = PesudoAlgorithm("FloydWarshall.txt")
        res["pageTitle"] = "Floyd-Warshall Algorithm"
        res["apiAlgo"] = "'floyd'"
    elif algorithm == "ford":
        algo = PesudoAlgorithm("BellmanFord.txt")
        res["pageTitle"] = "Bellman Ford Algorithm"
        res["apiAlgo"] = "'ford'"
    else:
        return render_to_response("algorithm_not_supported.html")

    res["jsonAlgo"] = json.dumps(algo.getJsonAlgo())
    return render_to_response("algorithm_base.html", res)
