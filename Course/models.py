from django.db import models

def change_image_path(instance , filepath):
    filepath = filepath.split('.')[-1]
    return f'CoursesImages/{instance.id}-{instance.Name}.{filepath}'
class Course(models.Model):
    Teacher = models.ForeignKey('Teacher.Teacher',on_delete=models.CASCADE)
    Name = models.CharField(max_length=200)
    Description = models.TextField()
    Price = models.IntegerField(null=True)
    Image = models.ImageField(upload_to= change_image_path, null=True)
    StateCourseChoices = (
        ('Active','Active'),
        ('Pause','Pause'),
        ('Completed','Completed')
    )
    StateCourse = models.CharField(choices=StateCourseChoices,max_length=20)

    def __str__(self):
        return self.Name

