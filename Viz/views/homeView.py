from Viz.utils.context import Context
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        cnt = Context().getContext()
        cnt["pageTitle"] = "Home"
        return cnt
