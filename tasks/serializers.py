from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, UserProfile


# -------------------------------
# USER REGISTRATION SERIALIZER
# -------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'mobile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        mobile = validated_data.pop('mobile')

        # Create user
        user = User.objects.create_user(**validated_data)

        # Create profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.mobile = mobile
        profile.save()

        return user


# -------------------------------
# USER CRUD SERIALIZER
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(source='userprofile.mobile')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile, created = UserProfile.objects.get_or_create(user=instance)
        profile.mobile = profile_data.get('mobile', profile.mobile)
        profile.save()

        return instance


# -------------------------------
# TASK SERIALIZER
# -------------------------------
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ['user']