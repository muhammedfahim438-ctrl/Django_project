from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, UserProfile


# ==================================
# USER REGISTRATION SERIALIZER
# ==================================
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

        user = User.objects.create_user(**validated_data)

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.mobile = mobile
        profile.save()

        return user


# ==================================
# USER CRUD SERIALIZER + IMAGE
# FINAL FIX
# ==================================
class UserSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(
        required=False,
        allow_blank=True
    )

    image = serializers.ImageField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'image']

    def validate_username(self, value):
        if self.instance:
            if User.objects.exclude(
                id=self.instance.id
            ).filter(
                username=value
            ).exists():
                raise serializers.ValidationError(
                    "Username already exists."
                )
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)

        profile, created = UserProfile.objects.get_or_create(
            user=instance
        )

        data['mobile'] = profile.mobile

        if profile.image:
            data['image'] = profile.image.url
        else:
            data['image'] = None

        return data

    def update(self, instance, validated_data):
        mobile = validated_data.pop('mobile', None)
        image = validated_data.pop('image', None)

        # Update User table
        if 'username' in validated_data:
            instance.username = validated_data['username']

        if 'email' in validated_data:
            instance.email = validated_data['email']

        instance.save()

        # Update Profile table
        profile, created = UserProfile.objects.get_or_create(
            user=instance
        )

        if mobile is not None:
            profile.mobile = mobile

        if image is not None:
            profile.image = image

        profile.save()

        return instance


# ==================================
# TASK SERIALIZER
# ==================================
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ['user']