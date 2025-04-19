from django.urls import path
from .views import get_users, create_user, user_detail,movies, now_playing, upcoming_movies, home_page, payment_checkout, payment_confirm, payment_third_party, payment_methods



urlpatterns  = [
    path('users/me', get_users, name='get_users'),
    path('users/register/', create_user, name='create_user'),
    path('users/<int:pk>/', user_detail, name='user_detail'),
    path('movies/', movies, name='movies'),
    path('movies/<int:pk>/', movies, name='movie_detail'),
    path('movies/now-playing/', now_playing, name='now_playing'),
    path('movies/upcoming/', upcoming_movies, name='upcoming_movies'),
    path('home/', home_page, name='home_page'),
    path('payments/checkout/', payment_checkout, name='payment_checkout'),
    path('payments/confirm/', payment_confirm, name='payment_confirm'),
    path('payments/third-party/', payment_third_party, name='payment_third_party'),
    path('payments/methods/', payment_methods, name='payment_methods'),
    
]