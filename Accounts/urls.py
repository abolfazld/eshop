from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('auth/' , views.LoginRegister , name='auth'),
    path('register/' , views.RegisterView , name='register'),
    path('login/' , views.LoginView , name='login'),
    path('logout/' , views.LogoutView , name='logout'),
]