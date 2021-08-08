from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .forms import RegisterForm


def LoginRegister(request): # TODO:BETTER NAME FOR THIS FUNC
    if request.user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    context = {
        'register_form' : form,
    }
    if request.user.is_authenticated:
        print('You are login in already')
    return render(request , 'accounts/login-register.html' , context)

# TODO : write better messages for views

def LoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request , username=email , password=password) # we should pass email for login
        if user is not None:
            login(request,user)
            messages.success(request,'You are successfully logged in !!')
            return redirect('/')
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
