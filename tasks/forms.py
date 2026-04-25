from django import forms
from django.contrib.auth.models import User
from .models import Task, UserProfile


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    mobile = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                mobile=self.cleaned_data['mobile']
            )

        return user


class UserEditForm(forms.ModelForm):
    mobile = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['mobile'].initial = self.instance.userprofile.mobile

    def save(self, commit=True):
        user = super().save(commit)

        user.userprofile.mobile = self.cleaned_data['mobile']
        user.userprofile.save()

        return user