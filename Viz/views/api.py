import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from djongo.sql2mongo import SQLDecodeError

from Viz.algorithms.Dijkstra import Dijkstra
from Viz.Graph.Graph import Graph
from Viz.algorithms.Floyd import FloydWarshall
from Viz.algorithms.Ford import BellmanFord
from Viz.models import Questions, Quiz, QuizScores, AttemptedQuestion
from Viz.utils.context import NodeEdgeSerializer
from users.models import CustomUser

context: dict = dict()
"""
This really should be in a seprate app 
"""

def graphFromQuiz(request: WSGIRequest, id):
    try:
        q = Quiz.objects.get(id=id)
    except Quiz.DoesNotExist:
        err = JsonResponse({"errmsg": "Invalid Quiz Id"})
        err.status_code = 404
        return err
    ret = q.graph.getJavaScriptData()
    err = JsonResponse(json.loads(json.dumps(ret, default=NodeEdgeSerializer)))
    err.status_code = 200
    return err


def randomGraph(request: WSGIRequest):
    numberOfNodes = request.GET.get("numberOfNodes", 7)
    isNegativeEdges = True if request.GET.get("isNegativeEdges", 'false') == 'true' else False
    ret = Graph.generateRandomGraph(numberOfNodes, isNegativeEdges=isNegativeEdges).getJavaScriptData()
    err = JsonResponse(json.loads(json.dumps(ret, default=NodeEdgeSerializer)))
    err.status_code = 200
    return err


def getAlgorithm(request: WSGIRequest, algorithm, source=None) -> HttpResponse:
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

    return JsonResponse(json.loads(json.dumps(ret, default=NodeEdgeSerializer)))


def tutorials(request):
    if request.user.is_authenticated:
        score = 0
        maxScore = 0
        put = json.loads(request.body)
        attemptedQs = []
        userObj = CustomUser.objects.get(id=request.user.id)
        quiz = Quiz.objects.get(id=put['quizId'])

        for i in put['result']:
            maxScore += 1
            question = Questions.objects.get(id=i['qId'])
            mark = 1 / len(question.answers)
            attemptedQuestion = AttemptedQuestion.objects.create(user=userObj, question=question, attempted_answers=i['ans'])
            attemptedQuestion.save()
            attemptedQs.append(attemptedQuestion)
            if len(i['ans']) > len(question.answers):
                continue  # Give 0 marks if the choose more answers than possible
            for answer in i['ans']:
                convertedAns = str(answer)
                if convertedAns in question.answers:
                    score += mark
        percent = (score / maxScore) * 100
        try:
            qzScore = QuizScores.objects.create(user=userObj, quiz=quiz, score=score, max_score=maxScore)
            for i in attemptedQs:
                qzScore.attempted_answers.add(i)
            qzScore.save()
        except SQLDecodeError as e:
            response = JsonResponse({"errmsg": "Quiz Already Completed cannot submit score again"})
            response.status_code = 400
            return response

        print("{}%".format(percent), userObj, quiz)
        response = JsonResponse({"msg": "Score saved"})
        response.status_code = 200
    else:
        response = JsonResponse({"msg": "User not authenticated"})
        response.status_code = 401
    return response
