from django.shortcuts import render
from django.http import JsonResponse , HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Config.Tools import ValidationText
from .models import Teacher
import json

def LoginRegister(request):
    return render(request,'LoginRegister.html')

@csrf_exempt
def LoginCheck(request):
    Context = {}
    Data = json.loads(request.body)
    UserName = Data.get('UserName') or None
    Password = Data.get('Password') or None

    if ValidationText(UserName, 4, 100, True) and ValidationText(Password, 7, 100, True):
        StateTeacher = Teacher.objects.filter(UserName=UserName,Password=Password).first()
        if StateTeacher != None:
            Context = StateTeacher.DecodeUserNameAndPassword()
            Context['Status'] = '200'
        else:
            Context['Status'] = '404'
    else:
        Context['Status'] = '204'

    return JsonResponse(Context)


@csrf_exempt
def RegisterCheck(request):
    Context = {}
    Data = json.loads(request.body)
    UserName = Data.get('UserName') or None
    Email = Data.get('Email') or None
    Password = Data.get('Password') or None
    if ValidationText(UserName,4,100,True) and ValidationText(Email,4,65) and ValidationText(Password,7,100,True):
        TeacherExists = Teacher.objects.filter(UserName=UserName).first()
        if TeacherExists == None:
            StateTeacher = Teacher.objects.create(UserName=UserName,Email=Email,Password=Password)
            Context = StateTeacher.DecodeUserNameAndPassword()
            Context['Status'] = '200'
        else:
            Context['Status'] = '409' # Teacher is Exists
    else:
        Context['Status'] = '204' # No Content or Content Is Wrong

    return JsonResponse(Context)