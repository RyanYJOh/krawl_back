from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    # path('api', views.apiOverview),
    path('', views.getAllPosts),
    path('post-content/', views.post),
    path('get-post/<int:pk>/', views.getThisPost),
    path('get-popular-posts/', views.getPopular),
    path('likes/', views.postLike), 
    path('likes/<int:pk>/', views.getDelLike),
    path('post-comment/', views.postComment),
    path('get-comment/<int:pk>/', views.getComments),
    path('del-comment/<int:pk>/', views.delComment),
    path('auth', include('rest_framework.urls', namespace='rest_framework'))
]