from django.urls import path
from .views import get_tweets_of_city, get_names_of_city, register_user

urlpatterns = [
    path('register', register_user, name='register_user'),
    path('tweets/<str:city>', get_tweets_of_city, name='get_tweets_of_city'),
    path('cities', get_names_of_city, name='get_names_of_city')
]
