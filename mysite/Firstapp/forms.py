from django import forms
import re
from django.contrib.auth.models import User



class RegistrationForm (forms.Form):
    username = forms.CharField(
        label= 'Username', 
        max_length = 20,
        widget= forms.TextInput(attrs={'placeholder': 'Nhập tên tài khoản', 'class': 'form-control', 'autofocus': True}))
    email = forms.EmailField(
        label= 'Email', 
        widget= forms.EmailInput(attrs={'placeholder': 'Nhập email', 'class': 'form-control'}))
    password = forms.CharField(
        label= 'Password', 
        min_length= 6, 
        max_length= 12, 
        widget= forms.PasswordInput(attrs={'placeholder': 'Nhập mật khẩu', 'class': 'form-control'}))
    confirm_password = forms.CharField(
        label= 'Confirm password', 
        min_length= 6, 
        max_length= 12, 
        widget= forms.PasswordInput(attrs={'placeholder': 'Nhập lại mật khẩu', 'class': 'form-control'}))


    def clean_username(self):
        un = self.cleaned_data.get('username')
        if not re.fullmatch(r'^\w+$', un):
            raise forms.ValidationError('Tên có kí tự không hợp lệ!')
        if User.objects.filter(username=un).exists():
            raise forms.ValidationError('Tên đã tồn tại!')
        return un
        
    
    def clean(self):
        cleaned_data = super().clean()
        pw = self.cleaned_data.get('password')
        cf_pw = self.cleaned_data.get('confirm_password')
        if pw != cf_pw:
            raise forms.ValidationError('Mật khẩu không khớp!')
        return cleaned_data
    

    def save(self):
        User.objects.create_user(
            username= self.cleaned_data.get('username'),
            email= self.cleaned_data.get('email'),
            password= self.cleaned_data.get('pasword'),
        )
    




