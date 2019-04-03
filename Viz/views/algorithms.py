import json
from Viz.algorithms.pesudo_algorithms.algorithmExporter import PesudoAlgorithm
from Viz.utils.context import Context

from django.views.generic import TemplateView

DIJKSTRA = "dijkstra"
FORD = "ford"
FLOYD = "floyd"
ALGORITHMS = [FORD, FLOYD, DIJKSTRA]


class AlgorithmView(TemplateView):
    template_name = "algorithm_base.html"

    def dispatch(self, request, *args, **kwargs):
        algorithm = kwargs.get("algorithm", "")
        if algorithm not in ALGORITHMS:
            self.template_name = "algorithm_not_supported.html"
        return super(AlgorithmView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        algorithm = kwargs.get("algorithm")
        if algorithm not in ALGORITHMS:
            return
        res = Context().getContext()
        pesudoAlgo = None
        if algorithm == DIJKSTRA:
            pesudoAlgo = PesudoAlgorithm("Dijkstra.txt")
            res["jsonAlgo"] = json.dumps(pesudoAlgo.getJsonAlgo())
            res["pageTitle"] = "Dijkstra Algorithm"
            res["apiAlgo"] = "'dijkstra'"
        elif algorithm == FLOYD:
            pesudoAlgo = PesudoAlgorithm("FloydWarshall.txt")
            res["pageTitle"] = "Floyd-Warshall Algorithm"
            res["apiAlgo"] = "'floyd'"
            res["isSourceNeeded"] = False
        elif algorithm == FORD:
            pesudoAlgo = PesudoAlgorithm("BellmanFord.txt")
            res["pageTitle"] = "Bellman Ford Algorithm"
            res["apiAlgo"] = "'ford'"

        res["jsonAlgo"] = json.dumps(pesudoAlgo.getJsonAlgo())
        return res
