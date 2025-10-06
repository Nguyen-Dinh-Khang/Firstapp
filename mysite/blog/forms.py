from django import forms
import re
from .models import Post, Author
from django.contrib.auth.models import User



class PostForm (forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'context', 'post']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Nhập tiêu đề',
                'class': 'form-control',
                'autofocus': True}),
            'context': forms.Textarea(attrs={
                'placeholder': 'Nhập nội dung',
                'class': 'form-control',
                'rows': 5}),
            'post': forms.ClearableFileInput(attrs={
                'class': 'form-control'})
                }
        





