from django import forms
from .models import User
from django.contrib import messages

class RegisterForm(forms.Form):
    username = forms.CharField()
    email= forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data

        password = data.get('password')
        password2 = data.get('confirm_password')

        is_user_exist =User.objects.filter(username=data.get('username')).first()
        is_email_exist = User.objects.filter(email=data.get('email')).first()

        if is_user_exist:
            raise forms.ValidationError('This username is taken')

        if is_email_exist:
            raise forms.ValidationError('This email is taken')

        if password != password2:
            raise forms.ValidationError('You password are not same') # TODO : BETTER MESSAGE


        return data

    def save(self ):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = User.objects.create(username=username , email=email)
        user.set_password(password)

        user.save()
