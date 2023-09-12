"""
Users API version 1 endpoints.
"""
from django.urls import path, include

from project.apps.users.api.v1 import views


app_name = 'v1'
urlpatterns = [
    path('create-user/', views.CreateUserView.as_view(), name='create-user')
]
