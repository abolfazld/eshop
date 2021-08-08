from django.urls import path , include
from .views import *
urlpatterns = [
    path('Login-Register',LoginRegister),
    path('Login-Register/RegisterCheck',RegisterCheck),
    path('Login-Register/LoginCheck',LoginCheck),
]