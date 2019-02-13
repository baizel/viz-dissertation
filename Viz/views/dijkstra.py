import json

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render_to_response
from django.http import HttpResponse
from Viz.pesudo_algorithms.algorithmExporter import Algorithm

from Viz.utils.context import Context

context: dict = dict()


def index(request: WSGIRequest) -> HttpResponse:
    cntx = Context()
    algo = Algorithm("Dijkstra.txt")
    res = cntx.getContext()
    res["jsonAlgo"] = json.dumps(algo.getJsonAlgo())
    print(json.dumps(algo.getJsonAlgo()))
    return render_to_response("dijkstra.html", res)
