from django.db import models
from Config.Security import Decode , UnDecode

class Teacher(models.Model):
    NameAndFamily = models.CharField(max_length=200,null=True,blank=True)
    PhoneNumber = models.CharField(max_length=20,null=True,blank=True)
    Email = models.CharField(max_length=65,null=True,blank=True)
    AboutMe = models.TextField(null=True,blank=True)
    UserName = models.CharField(max_length=100, null=True, blank=True)
    Password = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.NameAndFamily or 'Teacher'

    def DecodeUserNameAndPassword(self):
        # QlYSqVS_ : UserName
        # YPtIeRC_ : Password
        D = {
            'QlYSqVS_' : Decode(self.UserName),
            'YPtIeRC_' : Decode(self.Password)
        }
        return D

