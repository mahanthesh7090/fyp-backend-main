from django.urls import path
from .views import test_endpoint

urlpatterns = [
    path('', test_endpoint, name="test_endpoint"),
    
]
