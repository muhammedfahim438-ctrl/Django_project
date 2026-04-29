from django.urls import path
from .views import (
    auth_page,
    dashboard,
    edit_task,
    complete_task,
    delete_task,
    delete_user,
    logout_view,
)

urlpatterns = [
    # -------------------------
    # AUTH PAGE
    # -------------------------
    path('', auth_page, name='auth'),

    # -------------------------
    # DASHBOARD
    # -------------------------
    path('dashboard/', dashboard, name='dashboard'),

    # -------------------------
    # TASK ACTIONS
    # -------------------------
    path('task/edit/<int:id>/', edit_task, name='edit_task'),
    path('task/complete/<int:id>/', complete_task, name='complete_task'),
    path('task/delete/<int:id>/', delete_task, name='delete_task'),

    # -------------------------
    # USER ACTIONS
    # -------------------------
    path('user/delete/<int:id>/', delete_user, name='delete_user'),

    # -------------------------
    # LOGOUT
    # -------------------------
    path('logout/', logout_view, name='logout'),
]