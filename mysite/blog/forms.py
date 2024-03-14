from .models import Comment, Post
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','short_description','image','tags')
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
    "id":"inputLogin",
    "class":"form-control",
    "placeholder":"user",})
	)
    password=forms.CharField(widget=forms.PasswordInput(attrs={
    "type" : "password",
    "id": "inputPassword",
    "class":"form-control",
    "placeholder":"0000"}))
