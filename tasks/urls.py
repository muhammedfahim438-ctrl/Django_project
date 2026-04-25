from django.urls import path
from .views_api import (
    RegisterView,
    TaskListCreateAPI,
    TaskDetailAPI,
    TaskToggleCompleteAPI,
    UserListAPI,
    UserDetailAPI
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

    path('tasks/', TaskListCreateAPI.as_view()),
    path('tasks/<int:id>/', TaskDetailAPI.as_view()),
    path('tasks/<int:id>/toggle/', TaskToggleCompleteAPI.as_view()),

    path('users/', UserListAPI.as_view()),
    path('users/<int:id>/', UserDetailAPI.as_view()),
]