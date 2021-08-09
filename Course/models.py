from django.db import models

class Course(models.Model):
    Teacher = models.ForeignKey('Teacher.Teacher',on_delete=models.CASCADE)
    Name = models.CharField(max_length=200)
    Description = models.TextField()
    StateCourse = (
        ('Active','Active'),
        ('Pause','Pause'),
        ('Completed','Completed')
    )
    StateCourse = models.CharField(choices=StateCourse,max_length=20)

    def __str__(self):
        return self.Name

