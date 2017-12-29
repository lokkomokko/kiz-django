from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views

from main.models import MedList
from . import views, models

urlpatterns = [
    path('', views.index, name="index"),
    path('sign', views.signup, name='signup'),
    path('delete/<item_id>', views.delete, name='delete' ),
    path('list', login_required(MedList.as_view()), name='list'),
    path('update/<pk>', login_required(models.MedUpdate.as_view()), name='update'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('password_reset/', auth_views.password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    path('api', views.api, name='api')
]