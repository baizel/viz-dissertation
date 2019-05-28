from allauth.account.views import LoginView
import json

from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator

from Viz.algorithms.pesudo_algorithms.algorithmExporter import PseudoAlgorithm
from Viz.utils.context import ALGORITHMS, DIJKSTRA, FLOYD, FORD

from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from Viz.models import Quiz, QuizScores, AttemptedQuestion
from Viz.utils.context import NodeEdgeSerializer, Context

# (https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement)
from Viz.utils.QuizEngine import QuizEngine
from users.models import CustomUser


def add_default_context(pageTitle=None):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if function.__name__ == "get_context_data":
                ret = function(*args, **kwargs)
                title = pageTitle
                if pageTitle is None:
                    try:
                        title = ret["pageTitle"]
                        ret.pop("pageTitle")
                    except KeyError:
                        raise KeyError("No PageTitle provided from parameter and key 'pageTitle' not found in the returned object from function {}".format(function.__name__))
                isSourceNeeded = True
                if "isSourceNeeded" in ret:
                    isSourceNeeded = ret["isSourceNeeded"]
                    ret.pop("isSourceNeeded")
                return dict(**ret, **Context(title, isSourceNeeded).getContext())
            return function(*args, **kwargs)

        return wrapper

    return decorator


class HomePageView(TemplateView):
    template_name = "home.html"

    @add_default_context("Home")
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class AboutPageView(TemplateView):
    template_name = "about.html"

    @add_default_context("About")
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class LogInView(LoginView):
    @add_default_context("Login")
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get("isDemo") is not None and kwargs.get("isDemo") == "demo":
            user = authenticate(request, username="demo", password="password")
            if user is not None:
                login(request, user)
        return super().dispatch(request, *args, **kwargs)


class AlgorithmView(TemplateView):
    template_name = "algorithm_base.html"
    quizIds = []

    def dispatch(self, request, *args, **kwargs):
        algorithm = kwargs.get("algorithm", "")
        if request.user.is_authenticated:
            try:
                self.quizIds = list(QuizScores.objects.values("quiz_id").filter(user_id=request.user.id))
            except Quiz.DoesNotExist:
                pass

        if algorithm not in ALGORITHMS:
            self.template_name = "algorithm_not_supported.html"
        if algorithm == DIJKSTRA:
            self.template_name = 'dijkstra.html'
        return super().dispatch(request, *args, **kwargs)

    @add_default_context()
    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        algorithm = kwargs.get("algorithm")
        if algorithm not in ALGORITHMS:
            return

        res["quizIds"] = self.quizIds
        pesudoAlgo = None
        if algorithm == DIJKSTRA:
            pesudoAlgo = PseudoAlgorithm("Dijkstra.txt")
            res["jsonAlgo"] = json.dumps(pesudoAlgo.getJsonAlgo())
            res["pageTitle"] = "Dijkstra Algorithm"
            res["apiAlgo"] = DIJKSTRA
        elif algorithm == FLOYD:
            pesudoAlgo = PseudoAlgorithm("FloydWarshall.txt")
            res["pageTitle"] = "Floyd-Warshall Algorithm"
            res["apiAlgo"] = FLOYD
            res["isSourceNeeded"] = False
        elif algorithm == FORD:
            pesudoAlgo = PseudoAlgorithm("BellmanFord.txt")
            res["pageTitle"] = "Bellman Ford Algorithm"
            res["isNegativeEdges"] = True
            res["apiAlgo"] = FORD

        res["jsonAlgo"] = json.dumps(pesudoAlgo.getJsonAlgo())
        return res


class SummaryView(TemplateView):
    template_name = "quiz_summary.html"
    user = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    @add_default_context("Summary")
    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(id=self.user.id)
        allScores = QuizScores.objects.filter(user=user)
        totalScoreAchieved = 0
        totalPossibleScore = 0
        totalPercent = 0
        recentQuiz = allScores[0] if len(allScores) != 0 else None
        recentAtemptedAns = []
        i: QuizScores
        timeChartData = []
        for i in allScores:
            if i.date > recentQuiz.date:
                recentQuiz = i
            totalScoreAchieved += float(i.score)
            totalPossibleScore += float(i.max_score)
            totalPercent += float(i._percent)
            timeChartData.append({"date": i.date.timestamp() * 1000, "y": i.score})
        percentage = (totalScoreAchieved / totalPossibleScore) * 100 if totalPossibleScore != 0 else 0
        averagePerQuiz = totalPercent / len(allScores) if len(allScores) != 0 else 0
        stats = [
            {"Current score": "{}/{} ({:5.2f}%)".format(totalScoreAchieved, totalPossibleScore, percentage)},
            {"Number of Quiz's Completed": len(allScores)},
            {"Average Score  per quiz": "{:5.2f}%".format(averagePerQuiz)},
        ]
        quiz = None
        if recentQuiz is not None:
            quiz = Quiz.objects.get(id=recentQuiz.quiz.id)
            stats.append({"Recent Quiz Score": "{:5.2f}%".format((float(recentQuiz.score) / float(recentQuiz.max_score)) * 100)})
        exData = {}
        if quiz is not None:
            preface = quiz.preface
            exData = {"quizID": quiz.id, "preface": preface, "sourceNode": quiz.sourceNode}
            for i in quiz.questions.all():
                try:
                    a = AttemptedQuestion.objects.get(user_id=user.id, question_id=i.id)
                    recentAtemptedAns.append({"attemptedAns": a.attempted_answers, "question": i.getSummaryContext()})
                except AttemptedQuestion.DoesNotExist:
                    pass
                except AttemptedQuestion.MultipleObjectsReturned:
                    pass
        data = {"wrong": totalPossibleScore - totalScoreAchieved, "right": totalScoreAchieved, "stats": stats, "quiz": recentAtemptedAns, "timeChartData": timeChartData}
        data = dict(**data, **exData, **res)
        return data


class TutorialView(TemplateView):
    template_name = "tutorial.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @add_default_context("Tutorial")
    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        quiz = QuizEngine()
        graph = quiz.graph
        algo = quiz.getPesudoJSONAlgorithm()
        quiz = quiz.generateQuiz(3)  # TODO: Add LOD (level of difficulty)
        data = {"test": json.dumps(graph.getJavaScriptData(), default=NodeEdgeSerializer),
                "jsonAlgo": json.dumps(algo), "preface": quiz.preface, "questionsjs": json.dumps(quiz.getJsonFrontEndContext()),
                "quiz": quiz.getJsonFrontEndContext(), "sourceNode": quiz.sourceNode}

        return dict(**data, **res)
