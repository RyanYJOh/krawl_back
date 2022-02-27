from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    # path('api', views.apiOverview),
    path('', views.getAllPosts),
    path('post-content', views.post),
    path('likes', views.postLike), 
    path('likes/<int:pk>', views.getDelLike),
    path('auth', include('rest_framework.urls', namespace='rest_framework'))
]