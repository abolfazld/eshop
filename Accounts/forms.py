from django import forms
from .models import User
from django.contrib.auth import authenticate , login
class RegisterForm(forms.Form):
    username = forms.CharField()
    email= forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_confirm_password(self):
        data = self.cleaned_data

        password = data.get('password')
        password2 = data.get('confirm_password')

        is_user_exist =User.objects.filter(username=data.get('username')).first()

        if is_user_exist:
            raise forms.ValidationError('This username is taken')

        if password != password2:
            raise forms.ValidationError('You password are not same') # TODO : BETTER MESSAGE
        return data

    def clean_email(self):
        data = self.cleaned_data
        is_email_exist = User.objects.filter(email=data.get('email')).first()
        if is_email_exist:
            raise forms.ValidationError('This email is taken')
        return data.get('email')


    def clean_username(self):
        data = self.cleaned_data
        is_username_exist = User.objects.filter(username=data.get('username')).first()
        if is_username_exist:
            raise forms.ValidationError('This username is taken')
        return data.get('username')

    def save(self ):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = User.objects.create(username=username , email=email)
        user.set_password(password)

        user.save()

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password' , widget=forms.PasswordInput())

    def login_user(self , request): 
        data = self.cleaned_data
        user = authenticate(request , username= data.get('email') , password=data.get('password'))
        if user:
            login(request , user)
            return user
        return None