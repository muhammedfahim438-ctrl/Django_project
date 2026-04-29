from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Task, UserProfile


# ==================================
# TASK FORM
# ==================================
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'priority',
            'due_date'
        ]


# ==================================
# REGISTER FORM
# ==================================
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    mobile = forms.CharField(max_length=15)
    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email address'
        })
        self.fields['mobile'].widget.attrs.update({
            'placeholder': 'Mobile number'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password'
        })

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'mobile',
            'image',
            'password1',
            'password2'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            profile, created = UserProfile.objects.get_or_create(
                user=user
            )

            profile.mobile = self.cleaned_data['mobile']

            if self.cleaned_data.get('image'):
                profile.image = self.cleaned_data['image']

            profile.save()

        return user


# ==================================
# USER EDIT FORM
# ==================================
class UserEditForm(forms.ModelForm):
    mobile = forms.CharField(max_length=15)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        profile, created = UserProfile.objects.get_or_create(
            user=self.instance
        )

        self.fields['mobile'].initial = profile.mobile
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email address'
        })
        self.fields['mobile'].widget.attrs.update({
            'placeholder': 'Mobile number'
        })

    def save(self, commit=True):
        user = super().save(commit)

        profile, created = UserProfile.objects.get_or_create(
            user=user
        )

        profile.mobile = self.cleaned_data['mobile']

        if self.cleaned_data.get('image'):
            profile.image = self.cleaned_data['image']

        profile.save()

        return user
