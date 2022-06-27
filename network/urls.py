from django.urls import path

from network.views import *


urlpatterns = [
    path('register/', UserCreateAPIView.as_view()),
    path('user/', UserNetListView.as_view()),
    path('user/<int:pk>/', UserNetDetailView.as_view()),
    path('user/post-create/', PostCreateAPIView.as_view()), 
    path('posts/', PostNetListView.as_view()),
    path('posts/<int:pk>/', PostNetRetrieveAPIView.as_view()),
    path('posts/<int:pk>/update', PostNetUpdateView.as_view()),
    path('posts/<int:pk>/images/', PostImagesListAPIView.as_view()),
]
