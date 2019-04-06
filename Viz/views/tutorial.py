import json
import random
import secrets
from ast import literal_eval

import math
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Viz.Graph.Graph import Graph
from Viz.algorithms.Dijkstra import Dijkstra
from Viz.algorithms.DijkstraPseudoMapping import DijkstraPseudoMapping
from Viz.utils.context import customSerializer, NEIGHBOUR_NODE_COLOR


# (https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement)
def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])


@login_required
def view(request):
    quiz = QuizEngine()
    graph = quiz.graph
    algo = quiz.getPesudoJSONAlgorithm()
    return render(request, "tutorial.html",
                  context={"test": json.dumps(graph.getJavaScriptData(), default=customSerializer),
                           "jsonAlgo": json.dumps(algo), "preface": quiz.preface, "questionsjs": json.dumps(quiz.generateQuestions(6)),"questions": quiz.generateQuestions(6)})


class QuizEngine:
    NO_NEIGHBOUR_OPTION = "No Neighbour"
    INF_OPTIONS = str(float("inf"))

    def __init__(self):
        self.__maxNodes = 5
        self.graph = Graph.generateRandomGraph(self.__maxNodes)
        self.sourceNode = random.randint(1, self.__maxNodes)
        self.__algo = Dijkstra(self.graph, self.sourceNode)
        self.__animationEngine = self.__algo.getAnimationEngine()
        self.__nodeStateOrder = self.__animationEngine.nodeOrder
        self.__distanceState = {}
        self.__populateStates()
        self.preface = '''
                       Given the graph below & source node to be {}, answer the questions below<br>
                       Note: when choosing the node with the smallest distance on line 15, 
                       if the nodes in Q have the same distances then choose the node that comes next in order i.e (1,2,3...)
                       '''.format(self.sourceNode)

        self.__questionGenerators = [self.generateDistanceOfRandomNodeQuestion, self.generateCurrentNodeQuestion, self.generateNeighbourQuestions]
        self.generateQuestions(10)

    def generateQuestions(self, numberOfQs):
        questions = []
        for i in range(numberOfQs):
            qsGen = secrets.choice(self.__questionGenerators)
            qs = qsGen()
            questions.append(qs)
            print(qs)
        return questions

    def __populateStates(self):
        frame = self.__animationEngine.getFrames()
        iterationCounter = 0
        for i in frame["updates"]:
            if i['data'] is not None and i['data']['updateData'] is not None:
                for j in i['data']['updateData']:
                    if j['classID'] == DijkstraPseudoMapping.cmpCostID:
                        iterationCounter += 1
                    if j['classID'] == DijkstraPseudoMapping.distanceId and j['rawData'] is not None:
                        rep = j['rawData']
                        rep = rep.replace("inf", "'inf'")
                        dictionary = literal_eval(rep)
                        if len(dictionary) >= self.__maxNodes and 0 in dictionary.values():
                            self.__distanceState[iterationCounter] = dictionary

    def generateCurrentNodeQuestion(self):
        iteration = random.randint(0, self.__maxNodes - 1)
        baseQuestion = "On the {} iteration of the while Loop in the Dijkstra Algorithm (Line 14-24), what is the current node (variable 'u' on Line 15)?".format(ordinal(iteration))
        ansIndex = iteration * 2
        ans = list(self.__nodeStateOrder[ansIndex].values())[0][0]['id']
        options = [i for i in range(1, self.__maxNodes + 1)]
        return {"qs": baseQuestion, "ans": ans, "choices": options, "isMultipleChoice": False}

    def generateNeighbourQuestions(self):
        iteration = random.randint(0, self.__maxNodes - 1)
        baseQuestion = "On the {} iteration of the while Loop in the Dijkstra Algorithm (Line 14-24), what are the neighbours node(s) of the current node?".format(ordinal(iteration))
        ansIndex = (iteration * 2) + 1
        ans = []
        for i in list(self.__nodeStateOrder[ansIndex].values())[0]:
            if i["color"] == NEIGHBOUR_NODE_COLOR:
                ans.append(i['id'])
        if len(ans) <= 0:
            ans.append(self.NO_NEIGHBOUR_OPTION)

        options = [str(i) for i in range(1, self.__maxNodes + 1)]
        options.append(self.NO_NEIGHBOUR_OPTION)
        return {"qs": baseQuestion, "ans": ans, "choices": options, "isMultipleChoice": True}

    def generateDistanceOfRandomNodeQuestion(self):
        iteration = random.randint(1, self.__maxNodes - 1)
        randomNode = random.randint(1, self.__maxNodes)
        question = "On the {} iteration of the while Loop in the Dijkstra Algorithm (Line 14-24),whats the distance for node {}?".format(ordinal(iteration), randomNode)
        ans = self.__getNodeDistanceAtState(self.__distanceState, iteration)[randomNode]
        options = [str(random.randint(0, 50)) for _ in range(4)]
        options.append(str(ans))
        if str(ans) != self.INF_OPTIONS:
            options.append(self.INF_OPTIONS)
        random.shuffle(options)
        return {"qs": question, "ans": ans, "choices": options, "isMultipleChoice": False}

    def getPesudoJSONAlgorithm(self):
        return self.__animationEngine.pesudoAlgorithm.getJsonAlgo()

    def __getNodeDistanceAtState(self, states, stateNumber):
        if states.get(stateNumber) is None and stateNumber != 0:
            i = stateNumber - 1
            return self.__getNodeDistanceAtState(states, i)
        return states[stateNumber]
