from django.shortcuts import render_to_response
from django.http import HttpResponse

from Viz.utils.context import Context
from Viz.models import Book

context: dict = dict()


def index(request) -> HttpResponse:
    cntx = Context()

    p = Book.objects.createBook("namehello")
    p.save()
    # print(p);
    return render_to_response("base.html", cntx.getContext())
    # return HttpResponse("Hello, world. You're at the polls index.")
