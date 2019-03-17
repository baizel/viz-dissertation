from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render_to_response
from django.http import HttpResponse

from Viz.utils.context import Context
from Viz.models import Book

context: dict = dict()


def index(request: WSGIRequest) -> HttpResponse:
    cntx = Context()

    # p = Book.objects.createBook("namehello")
    # p.save()
    return render_to_response("home.html", cntx.getContext())
    # return HttpResponse("Hello, world. You're at the polls index.")
