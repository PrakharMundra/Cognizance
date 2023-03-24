from django.urls import path
from . import views


urlpatterns = [
    path('splitwise/auth/', views.splitwise_auth, name='splitwise_auth'),
    # Add more URL patterns as needed
    path('', views.home, name='splitWise-home'),
]
