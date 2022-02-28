from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('api', views.apiOverview),
    path('', views.account_list),
    path('register', views.register),
    path('<int:pk>', views.account),
    path('rankings', views.getRankings),
    path('navbar', views.navbar),
    # path('login', views.login),
    path('auth', include('rest_framework.urls', namespace='rest_framework'))
]