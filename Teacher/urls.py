from django.urls import path , include
from .views import *
urlpatterns = [
    path('Panel', Panel),
    path('Panel/SubmitInformation',SubmitInformation),

    path('Login-Register',LoginRegister),
    path('Login-Register/RegisterCheck',RegisterCheck),
    path('Login-Register/LoginCheck',LoginCheck)


]