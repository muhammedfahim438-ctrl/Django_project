from django.contrib import admin
from django.urls import path, include
from tasks.views import register_view   # ✅ correct import

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django auth (login/logout)
    path('accounts/', include('django.contrib.auth.urls')),

    # Register page
    path('register/', register_view, name='register'),

    # HTML frontend (tasks)
    path('', include('tasks.urls_html')),

    # API backend
    path('api/', include('tasks.urls')),
]