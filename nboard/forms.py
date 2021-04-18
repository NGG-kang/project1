from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', 'photo']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']







