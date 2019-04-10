from allauth.account.views import LoginView
import json

from django.utils.decorators import method_decorator

from Viz.algorithms.pesudo_algorithms.algorithmExporter import PesudoAlgorithm
from Viz.utils.context import ALGORITHMS, DIJKSTRA, FLOYD, FORD

from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from Viz.models import Quiz, QuizScores, AttemptedQuestion
from Viz.utils.context import NodeEdgeSerializer, Context

# (https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement)
from Viz.utils.QuizEngine import QuizEngine
from users.models import CustomUser

context = Context().getContext()


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        cnt = Context().getContext()
        cnt["pageTitle"] = "Home"
        return cnt


class AboutPageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        cnt = Context().getContext()
        cnt["pageTitle"] = "About"
        return cnt


class LogInView(LoginView):
    def get_context_data(self, **kwargs):
        context = super(LogInView, self).get_context_data(**kwargs)
        ret = dict(**context, **Context().getContext())
        return ret


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

    def get_context_data(self, **kwargs):
        algorithm = kwargs.get("algorithm")
        if algorithm not in ALGORITHMS:
            return
        res = Context().getContext()
        res["quizIds"] = self.quizIds
        pesudoAlgo = None
        if algorithm == DIJKSTRA:
            pesudoAlgo = PesudoAlgorithm("Dijkstra.txt")
            res["jsonAlgo"] = json.dumps(pesudoAlgo.getJsonAlgo())
            res["pageTitle"] = "Dijkstra Algorithm"
            res["apiAlgo"] = DIJKSTRA
        elif algorithm == FLOYD:
            pesudoAlgo = PesudoAlgorithm("FloydWarshall.txt")
            res["pageTitle"] = "Floyd-Warshall Algorithm"
            res["apiAlgo"] = FLOYD
            res["isSourceNeeded"] = False
        elif algorithm == FORD:
            pesudoAlgo = PesudoAlgorithm("BellmanFord.txt")
            res["pageTitle"] = "Bellman Ford Algorithm"
            res["apiAlgo"] = FLOYD

        res["jsonAlgo"] = json.dumps(pesudoAlgo.getJsonAlgo())
        return res


class SummaryView(TemplateView):
    template_name = "quiz_summary.html"
    user = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = CustomUser.objects.get(id=self.user.id)
        allScores = QuizScores.objects.filter(user=user)
        totalScoreAchieved = 0
        totalPossibleScore = 0
        totalPercent = 0
        recentQuiz = allScores[0] if len(allScores) != 0 else None
        recentAtemptedAns = []

        for i in allScores:
            if i.date > recentQuiz.date:
                recentQuiz = i
            totalScoreAchieved += float(i.score)
            totalPossibleScore += float(i.max_score)
            totalPercent += float(i._percent)
        percentage = (totalScoreAchieved / totalPossibleScore) * 100 if totalPossibleScore != 0 else 0
        averagePerQuiz = totalPercent / len(allScores) if len(allScores) != 0 else 0
        stats = [
            {"Current score": "{}/{} ({:5.2f}%)".format(totalScoreAchieved, totalPossibleScore, percentage)},
            {"Number of Quiz's Completed": len(allScores)},
            {"Average Score  per quiz": "{:5.2f}%".format(averagePerQuiz)},
        ]
        quiz = None
        if recentQuiz is not None:
            print(recentQuiz.id)
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
        data = {"wrong": totalPossibleScore - totalScoreAchieved, "right": totalScoreAchieved, "stats": stats, "quiz": recentAtemptedAns}
        data = dict(**data, **exData, **context)
        return data


class TutorialView(TemplateView):
    template_name = "tutorial.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        quiz = QuizEngine()
        graph = quiz.graph
        algo = quiz.getPesudoJSONAlgorithm()
        quiz = quiz.generateQuiz(3)  # TODO: Add LOD (level of difficulty)
        data = {"test": json.dumps(graph.getJavaScriptData(), default=NodeEdgeSerializer),
                "jsonAlgo": json.dumps(algo), "preface": quiz.preface, "questionsjs": json.dumps(quiz.getJsonFrontEndContext()),
                "quiz": quiz.getJsonFrontEndContext(), "sourceNode": quiz.sourceNode}

        cntx = dict(**context, **data)
        return cntx
