from django.urls import path
from .views import get_users, create_user, user_detail, get_movies, create_movie, get_shows, create_shows, movies 


urlpatterns  = [
    path('users/', get_users, name='get_users'),
    path('users/register/', create_user, name='create_user'),
    path('users/<int:pk>/', user_detail, name='user_detail'),
    path('movies/', movies, name='movies'),
    path('movies/<int:pk>/', movies, name='movie_detail'),
    path('shows/', get_shows, name= 'get_shows'),
    path('shows/create/', create_shows, name='create_shows'),
]