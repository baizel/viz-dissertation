from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def view(request):
    return render(request, "tutorial.html")


class QuizEngine:
    pass
