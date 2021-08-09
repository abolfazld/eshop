from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Config.Tools import ValidationText, Set_Cookie_Functionality
from Config.User import GetUser_ByMODEL
from .models import Teacher
import json


def Panel(request):
    Context = {}
    StateTeacher = GetUser_ByMODEL(request, 'Teacher')
    if StateTeacher == None:
        return redirect('/t/Login-Register')
    Context['Teacher'] = StateTeacher
    return render(request, 'Panel.html', Context)


def SubmitInformation(request):
    Context = {}
    Status = 0
    Data = request.POST
    Teacher = GetUser_ByMODEL(request, 'Teacher')
    NameAndFamily = Data.get('NameAndFamily') or None
    Email = Data.get('Email') or None
    PhoneNumber = Data.get('PhoneNumber') or None
    AboutMe = Data.get('AboutMe') or None
    Image = request.FILES.get('Image') or None
    StateImage = Data.get('StateImage') or None

    if Teacher is not None:
        if ValidationText(NameAndFamily, 3, 200) and ValidationText(Email, 3, 65) and ValidationText(PhoneNumber, 3,
                                                                                                     20) and ValidationText(
            AboutMe, 2, 5000):
            Teacher.NameAndFamily = NameAndFamily
            Teacher.PhoneNumber = PhoneNumber
            Teacher.Email = Email
            Teacher.AboutMe = AboutMe
            Context['Status'] = '200'
            Status = 200
            if StateImage == 'MostGet' and Image == None:
                Status = 203
            elif StateImage == 'MostGet' and Image != None:
                Teacher.Image = Image

            Teacher.save()
        else:
            Context['Status'] = '204'
            Status = 204
    else:
        # Context['Status'] = '404'
        # Status = 404
        return redirect('/t/Login-Register')

    if Status == 200:
        return Set_Cookie_Functionality('Your information has been saved successfully', 'Success', 5000, '2',
                                        '/t/Panel?Information')
    if Status == 203:
        return Set_Cookie_Functionality('Photo not entered correctly. Please try again in a few minutes', 'Error', 6000,
                                        '2',
                                        '/t/Panel?Information')
    elif Status == 204:
        return Set_Cookie_Functionality('Please fill in the fields correctly', 'Error', 6000, '2',
                                        '/t/Panel?Information')
    return HttpResponse('')


def LoginRegister(request):
    return render(request, 'LoginRegister.html')


@csrf_exempt
def LoginCheck(request):
    Context = {}
    Data = json.loads(request.body)
    UserName = Data.get('UserName') or None
    Password = Data.get('Password') or None

    if ValidationText(UserName, 4, 100, True) and ValidationText(Password, 7, 100, True):
        StateTeacher = Teacher.objects.filter(UserName=UserName, Password=Password).first()
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
    if ValidationText(UserName, 4, 100, True) and ValidationText(Email, 4, 65) and ValidationText(Password, 7, 100,
                                                                                                  True):
        TeacherExists = Teacher.objects.filter(UserName=UserName).first()
        if TeacherExists == None:
            StateTeacher = Teacher.objects.create(UserName=UserName, Email=Email, Password=Password)
            Context = StateTeacher.DecodeUserNameAndPassword()
            Context['Status'] = '200'
        else:
            Context['Status'] = '409'  # Teacher is Exists
    else:
        Context['Status'] = '204'  # No Content or Content Is Wrong

    return JsonResponse(Context)
