from django.urls import path
from . import views as core_views
from . import views

urlpatterns = [
    path('/static', views.index, name="index"),
    path('', core_views.signup, name='signup')
]