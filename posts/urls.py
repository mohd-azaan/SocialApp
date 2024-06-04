from django.urls import path
from . import views
urlpatterns = [
    path('createPost/', views.create_post, name="createPost"),
    path('explore/', views.explore, name="explore"),
    path('like/', views.like_post, name="like"),
]
