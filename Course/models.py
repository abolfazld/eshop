from django.db import models
from Config.Tools import GetDifferenceTime
from django.utils import timezone
from datetime import timedelta , datetime
import cv2
import math
import requests


def UploadTo_ImageCourse(instance, path):
    return f'ImagesCourse/{instance.id}/{instance.Title}{path}'


def UploadTo_VideoCourse(instance, filename):
    Format = filename.split('.')
    Format = Format[len(Format)-1]
    return f'VideoCourse/{instance.Section.Course.Title}/Section_{instance.Section.id}/Video_{instance.id}.{Format}'


class VideoCourse(models.Model):
    Section = models.ForeignKey('Course.SectionCourse', on_delete=models.CASCADE)
    Video = models.FileField(upload_to=UploadTo_VideoCourse, null=True)
    DurationVideo = models.CharField(max_length=20, null=True, blank=True)
    DateTimeSubmit = models.DateTimeField(auto_now_add=True)
    StateVideo = (
        ('200', '200'),
        ('400', '400')
    )
    StateVideo = models.CharField(max_length=30, choices=StateVideo)

    def __str__(self):
        return f'{self.Section.Course.Title}_{self.Section.id}_{self.id}'

    def GetDurationVideo(self):
        Duration = float(self.DurationVideo)
        if Duration != 0 and Duration > 0:
            Second = math.floor(Duration % 60)
            Minute = math.floor(Duration // 60)
            M = ''
            if Minute != 0:
                M = f'{Minute}m'
            Duration = f'{M} {Second}s'
            return Duration
        return '0s'

    def GetTimePastSubmit(self):
        return GetDifferenceTime(self.DateTimeSubmit)


class SectionCourse(models.Model):
    Course = models.ForeignKey('Course.Course', on_delete=models.CASCADE)
    Title = models.CharField(max_length=150)
    DateTimeSubmit = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Title

    def GetVideos(self):
        return VideoCourse.objects.filter(Section_id=self.id)

    def LenVideos(self):
        return VideoCourse.objects.filter(Section_id=self.id).__len__()


class Discount(models.Model):
    Course = models.ForeignKey('Course.Course',on_delete=models.CASCADE)
    Title = models.CharField(max_length=200,null=True,blank=True)
    Percent = models.CharField(max_length=5)
    Time = models.CharField(max_length=15)
    DateTimeSubmit = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.Course.Title}_{self.Time} hour'

    def TimeExpired(self):
        TimeSubmit = self.DateTimeSubmit
        Hour = int(self.Time)
        Res = (TimeSubmit + timedelta(hours=Hour))
        if datetime.now() > Res:
            self.delete()
        return str(Res)




def change_image_path(instance , filepath):
    filepath = filepath.split('.')[-1]
    return f'CoursesImages/{instance.id}-{instance.Name}.{filepath}'


class Course(models.Model):
    Teacher = models.ForeignKey('Teacher.Teacher', on_delete=models.CASCADE)
    Title = models.CharField(max_length=200)
    Description = models.TextField()
    StateCourse = (
        ('Active', 'Active'),
        ('Pause', 'Pause'),
        ('Completed', 'Completed')
    )
    PreRequisites = models.CharField(max_length=200)
    References = models.CharField(max_length=1000)
    StateCourse = models.CharField(choices=StateCourse, max_length=20)
    DateTimeSubmit = models.DateTimeField(auto_now_add=True)
    LastTimeUpdated = models.DateTimeField(null=True, blank=True)
    Image = models.ImageField(upload_to=UploadTo_ImageCourse, null=True)
    Price = models.CharField(max_length=15)


    def __str__(self):
        return self.Title

    def TimePastSubmit(self):
        return GetDifferenceTime(self.DateTimeSubmit)

    def TimePastUpdated(self):
        TimeUpdated = self.LastTimeUpdated
        if TimeUpdated != None and TimeUpdated != '':
            return GetDifferenceTime(TimeUpdated)
        return 'Unknown'

    def CourseIsFree(self):
        if self.Price == '0':
            return True
        return False

    def GetPrice(self):
        if self.Price == '0':
            return 'Free'
        else:
            if self.HasDiscount():
                Price = int(self.Price)
                return Price - (Price / 100) * int(self.GetDiscount().Percent)
            return self.Price

    def GetSections(self):
        return SectionCourse.objects.filter(Course_id=self.id)

    def UpdateTimeCourse(self):
        self.LastTimeUpdated = timezone.now()
        self.save()


    def HasDiscount(self):
        D = Discount.objects.filter(Course_id=self.id).first()
        return True if D != None else False

    def GetDiscount(self):
        return Discount.objects.filter(Course_id=self.id).first()

