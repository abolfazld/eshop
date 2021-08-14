from django.urls import path
from .views import home , course_detail

urlpatterns = [
    path('' , home , name='home') ,
    path('course/<int:pk>' , course_detail , name='course_detail') ,
]