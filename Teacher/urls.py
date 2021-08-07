
from django.urls import path , include
from .views import LoginRegister
urlpatterns = [
    path('',LoginRegister)
]