from django.db import models
from Config.Security import Decode , UnDecode
from Course.models import Course


def UploadTo(instance,filepath):
    filepath = filepath.split('.')[-1]
    return f'TeachersImages/{instance.id}-{instance.NameAndFamily}.{filepath}'


class Teacher(models.Model):
    NameAndFamily = models.CharField(max_length=200,null=True,blank=True)
    PhoneNumber = models.CharField(max_length=20,null=True,blank=True)
    Email = models.CharField(max_length=65,null=True,blank=True)
    AboutMe = models.TextField(null=True,blank=True)
    Image = models.ImageField(upload_to=UploadTo,null=True,blank=True)
    UserName = models.CharField(max_length=100, null=True, blank=True)
    Password = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.NameAndFamily or 'Teacher'

    def GetNameAndFamily(self):
        return self.__str__()

    def DecodeUserNameAndPassword(self):
        # QlYSqVS_ : UserName
        # YPtIeRC_ : Password
        D = {
            'QlYSqVS' : Decode(self.UserName),
            'YPtIeRC' : Decode(self.Password)
        }
        return D

    def GetAllCourse(self):
        return Course.objects.filter(Teacher_id=self.id)[::-1]

    def GetCoursesActive(self):
        return Course.objects.filter(Teacher_id=self.id,StateCourse='Active')[::-1]

    def GetCoursesPause(self):
        return Course.objects.filter(Teacher_id=self.id,StateCourse='Pause')[::-1]

    def GetCoursesCompleted(self):
        return Course.objects.filter(Teacher_id=self.id,StateCourse='Completed')[::-1]



