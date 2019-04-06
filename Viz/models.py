from django.db import models


# class MultipleChoiceQuestionManager(models.Manager):
#     def createQs(self, question, choices, answer):
#         qs = self.create(question=question, choices=choices, answer=answer)
#         # do something with the book
#         return qs
#
#
# class MultipleChoiceQuestion(models.Model):
#     question = models.CharField(max_length=250)
#
#     objects = MultipleChoiceQuestionManager()
