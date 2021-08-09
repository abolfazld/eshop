from django.shortcuts import redirect, render
from django.contrib.auth import  logout
from django.contrib import messages
from .forms import RegisterForm , LoginForm


def LoginRegister(request): # TODO:BETTER NAME FOR THIS FUNC
    if request.user.is_authenticated:
        return redirect('/')
    register_form = RegisterForm()
    login_form = LoginForm()
    context = {
        'register_form' : register_form,
        'login_form' : login_form,
    }
    if request.user.is_authenticated:
        print('You are login in already')
    return render(request , 'accounts/login-register.html' , context)

# TODO : write better messages for views

def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None) # we should pass email for login
        if form.is_valid():
            user = form.login_user(request)
            if user:
                messages.success(request,'You are successfully logged in !!')
                return redirect('/')
            messages.error(request , 'Email / password is incorrect')
    return redirect('accounts:auth')

def LogoutView(request):
    logout(request)
    messages.success(request , 'You are successfully logout !!')
    return redirect('/')

def RegisterView(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,'You are successfully made an account !!')
    return redirect('accounts:auth')
