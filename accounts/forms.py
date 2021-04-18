from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm
from .models import Profile


class UserForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['user_photo', 'status_message']