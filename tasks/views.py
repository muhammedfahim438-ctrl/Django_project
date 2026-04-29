import base64
import uuid

from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .models import Task, UserProfile
from .forms import RegisterForm, UserEditForm


# ==================================
# AUTH PAGE (LOGIN + REGISTER)
# ==================================
def auth_page(request):
    register_form = RegisterForm()
    login_error = ""
    image_data = ""

    # LOGIN
    if request.method == "POST" and "login_btn" in request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            login_error = "Invalid username or password"

    # REGISTER
    if request.method == "POST" and "register_btn" in request.POST:
        image_data = request.POST.get("image_data", "")
        register_form = RegisterForm(
            request.POST,
            request.FILES
        )

        if register_form.is_valid():
            user = register_form.save()

            if image_data and "base64," in image_data:
                profile, created = UserProfile.objects.get_or_create(
                    user=user
                )
                format_part, image_part = image_data.split("base64,", 1)
                extension = "png" if "png" in format_part else "jpg"
                profile.image.save(
                    f"profile-{uuid.uuid4()}.{extension}",
                    ContentFile(base64.b64decode(image_part)),
                    save=True
                )

            login(request, user)
            return redirect("dashboard")

    return render(request, "task/auth.html", {
        "register_form": register_form,
        "login_error": login_error,
        "image_data": image_data
    })


# ==================================
# DASHBOARD PAGE
# ==================================
@login_required
def dashboard(request):
    tasks = Task.objects.filter(
        user=request.user
    ).order_by("-created_at")

    UserProfile.objects.get_or_create(
        user=request.user
    )

    profile = request.user.userprofile
    profile_form = UserEditForm(instance=request.user)
    active_tab = "overview"
    show_profile_form = False

    if request.method == "POST" and "update_profile" in request.POST:
        active_tab = "profile"
        show_profile_form = True
        profile_form = UserEditForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if profile_form.is_valid():
            profile_form.save()

            return redirect("dashboard")

    # ADD TASK
    if request.method == "POST" and "add_task" in request.POST:
        title = request.POST.get("title")
        description = request.POST.get("description")

        Task.objects.create(
            user=request.user,
            title=title,
            description=description
        )

        return redirect("dashboard")

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    progress_percent = 0

    if total_tasks:
        progress_percent = round((completed_tasks / total_tasks) * 100)

    return render(
        request,
        "task/dashboard.html",
        {
            "tasks": tasks,
            "profile": profile,
            "profile_form": profile_form,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "progress_percent": progress_percent,
            "active_tab": active_tab,
            "show_profile_form": show_profile_form
        }
    )


# ==================================
# EDIT TASK
# ==================================
@login_required
def edit_task(request, id):
    task = get_object_or_404(
        Task,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.save()

    return redirect("dashboard")


# ==================================
# COMPLETE TASK
# ==================================
@login_required
def complete_task(request, id):
    task = get_object_or_404(
        Task,
        id=id,
        user=request.user
    )

    task.is_completed = True
    task.save()

    return redirect("dashboard")


# ==================================
# DELETE TASK
# ==================================
@login_required
def delete_task(request, id):
    task = get_object_or_404(
        Task,
        id=id,
        user=request.user
    )

    task.delete()

    return redirect("dashboard")


# ==================================
# DELETE USER
# ==================================
@login_required
def delete_user(request, id):
    if not request.user.is_superuser:
        return redirect("dashboard")

    user = get_object_or_404(User, id=id)
    user.delete()

    return redirect("dashboard")


# ==================================
# LOGOUT
# ==================================
def logout_view(request):
    logout(request)
    return redirect("auth")
