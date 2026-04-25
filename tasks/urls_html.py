from django.urls import path
from .views import (
    task_list,
    add_task,
    register_view,
    user_list,
    edit_user,
    delete_user
)

urlpatterns = [
    path('', task_list, name='task_list'),
    path('add/', add_task, name='add_task'),
    path('register/', register_view, name='register'),

    path('users/', user_list, name='user_list'),
    path('users/edit/<int:id>/', edit_user, name='edit_user'),
    path('users/delete/<int:id>/', delete_user, name='delete_user'),
]