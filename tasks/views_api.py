from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Task
from .serializers import RegisterSerializer, TaskSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer

# ===============================
# User Registration API
# ===============================
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ===============================
# Task List + Create API
# ===============================
class TaskListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ===============================
# Single Task API
# Get / Put / Patch / Delete
# ===============================
class TaskDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, id):
        return get_object_or_404(
            Task,
            id=id,
            user=request.user
        )

    # Get single task
    def get(self, request, id):
        task = self.get_object(request, id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    # Full update
    def put(self, request, id):
        task = self.get_object(request, id)
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Partial update
    def patch(self, request, id):
        task = self.get_object(request, id)
        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete task
    def delete(self, request, id):
        task = self.get_object(request, id)
        task.delete()

        return Response(
            {"message": "Task deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# ===============================
# Toggle Complete / Incomplete
# ===============================
class TaskToggleCompleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        task = get_object_or_404(
            Task,
            id=id,
            user=request.user
        )

        task.is_completed = not task.is_completed
        task.save()

        return Response({
            "id": task.id,
            "title": task.title,
            "completed": task.is_completed
        })
    # ===============================
# User CRUD API
# ===============================
class UserDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(
            {"message": "User deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    from django.contrib.auth.models import User
from .serializers import UserSerializer


class UserListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        return User.objects.get(id=id)

    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        user = self.get_object(id)
        user.delete()
        return Response({"message": "User deleted successfully"})