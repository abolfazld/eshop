from django.shortcuts import render ,get_object_or_404
from .models import Course

def home(request, *args , **kwargs):
    courses = Course.objects.all()
    context = {
        'courses' : courses ,
    }
    return render(request , 'index.html' , context)

def course_detail(request , pk , *args , **kwargs):
    course = get_object_or_404(Course , pk=pk)
    teacher = course.Teacher
    teacher_courses_count = teacher.course_set.count()
    context = {
        'course':course ,
        'teacher':teacher ,
        'teacher_courses_count':teacher_courses_count ,
    }
    return render(request , 'course-page.html' , context)