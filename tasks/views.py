from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User

from .models import Task
from .forms import TaskForm, RegisterForm, UserEditForm
from .models import UserProfile
from django.contrib.auth.models import User


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task/task_list.html', {'tasks': tasks})


@login_required
def add_task(request):
    form = TaskForm(request.POST or None)

    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('task_list')

    return render(request, 'task/add_task.html', {'form': form})


def register_view(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('task_list')

    return render(request, 'registration/register.html', {'form': form})


@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'task/user_list.html', {'users': users})


@login_required
def edit_user(request, id):
    user = User.objects.get(id=id)

    # Auto create profile if missing
    UserProfile.objects.get_or_create(user=user)

    form = UserEditForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect('user_list')

    return render(request, 'task/edit_user.html', {'form': form})


@login_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('user_list')