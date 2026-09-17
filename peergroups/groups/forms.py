from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Group, Comment, Photo

User = get_user_model()


class GroupForm(forms.ModelForm):
    # The HTML5 datetime-local input both displays and submits values shaped
    # like "2026-08-25T14:30" (a "T" separator, no seconds). Django's default
    # DATETIME_INPUT_FORMATS use a space separator, so without input_formats
    # here, editing a group would fail to parse the submitted time.
    meeting_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'],
        help_text="When you're meeting",
    )

    class Meta:
        model = Group
        fields = ['name', 'interest', 'description', 'location', 'meeting_time',  'office_hour', 'privacy']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Say something to the group...',
            }),
        }
        labels = {'text': ''}


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Caption (optional)'}),
        }
        labels = {'image': '', 'caption': ''}


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    """Lets a logged-in user change their username and email."""

    class Meta:
        model = User
        fields = ('username', 'email')
