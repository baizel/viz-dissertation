"""
VizApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from Viz.views import views, api

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    re_path(r'^favicon\.ico$', favicon_view),
    path('', views.HomePageView.as_view(), name="home"),
    path('summary/', views.SummaryView.as_view(), name="summary"),
    path('tutorial/', views.TutorialView.as_view(), name="tutorial"),
    path('about/', views.AboutPageView.as_view(), name="about"),
    path('algorithm/<str:algorithm>/', views.AlgorithmView.as_view(), name="algorithm"),
    path('api/tutorial/', api.tutorials),
    path('api/graph/random', api.randomGraph),
    path('api/graph/<int:id>', api.graphFromQuiz),
    path('api/animation/<str:algorithm>/', api.getAlgorithm),
    path('api/animation/<str:algorithm>/<int:source>', api.getAlgorithm),
    path('users/', include('users.urls')),  # new
    path('users/', include('django.contrib.auth.urls')),  # new
    url(r"^accounts/login/$", views.LogInView.as_view(), name="account_login"),
    path('accounts/', include('allauth.urls')),  # new
    path('admin/', admin.site.urls),
]
