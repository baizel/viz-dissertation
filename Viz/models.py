import json

from django.db import models
from django.utils import timezone

from Viz.Graph.Graph import Graph
from Viz.utils.context import NodeEdgeSerializer
from users.models import CustomUser


class AttemptedQuestionManager(models.Manager):
    pass


class QuizManager(models.Manager):
    pass


class QuizScoreManager(models.Manager):
    def create(self, *args, **kwargs):
        kwargs["_percent"] = kwargs['score'] / kwargs['max_score'] * 100
        kwargs["date"] = timezone.now()
        return super(QuizScoreManager, self).create(*args, **kwargs)


class QuestionsManger(models.Manager):
    pass


class Questions(models.Model):
    question = models.TextField(max_length=500)
    _answers = models.CharField(max_length=200)
    _choices = models.CharField(max_length=200)
    isMultipleChoice = models.BooleanField()
    objects = QuestionsManger()

    @property
    def answers(self):
        return [str(i) for i in json.loads(self._answers)]

    @answers.setter
    def answers(self, x):
        if not isinstance(x, list):
            raise ValueError("Expected type list but got {}".format(type(x)))
        self._answers = json.dumps(x)

    @property
    def choices(self):
        return [str(i) for i in json.loads(self._choices)]

    @choices.setter
    def choices(self, x):
        self._choices = json.dumps(x)

    def getSummaryContext(self):
        return {"id": self.id, "qs": self.question, "answers": self.answers, "choices": self.choices, "isMultipleChoice": self.isMultipleChoice}

    def getJsonForFrontEnd(self):
        # Dont include answers when using it for front end
        return {"id": self.id, "qs": self.question, "choices": self.choices, "isMultipleChoice": self.isMultipleChoice}


class Quiz(models.Model):
    preface = models.TextField(max_length=500)
    questions = models.ManyToManyField(Questions)
    _graph = models.TextField(max_length=1000)
    sourceNode = models.IntegerField()
    objects = QuizManager()

    @property
    def graph(self):
        return Graph(json.loads(self._graph))

    @graph.setter
    def graph(self, x):
        self._graph = json.dumps(x, default=NodeEdgeSerializer)

    def getJsonSummaryContext(self):
        qs = []
        for i in self.questions.all():
            qs.append(i.getSummaryContext())
        return {"id": self.id, "questions": qs}

    def getJsonFrontEndContext(self):
        qs = []
        for i in self.questions.all():
            qs.append(i.getJsonForFrontEnd())
        return {"id": self.id, "questions": qs}


class AttemptedQuestion(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE,
    )
    _attempted_answers = models.CharField(max_length=100, db_column="attempted_answers")
    objects = AttemptedQuestionManager()

    @property
    def attempted_answers(self):
        return [str(i) for i in json.loads(self._attempted_answers)]

    @attempted_answers.setter
    def attempted_answers(self, x):
        if not isinstance(x, list):
            raise ValueError("Expected type list but got {}".format(type(x)))
        self._attempted_answers = json.dumps(x)


class QuizScores(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
    )

    attempted_answers = models.ManyToManyField(AttemptedQuestion)

    score = models.DecimalField(max_digits=10, decimal_places=4)
    max_score = models.DecimalField(max_digits=10, decimal_places=4)
    _percent = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(editable=False)
    objects = QuizScoreManager()

    class Meta:
        unique_together = (("user", "quiz"),)
