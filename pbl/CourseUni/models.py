from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class courses(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=200)
    img = models.ImageField(upload_to="pics")
    des = models.CharField(max_length=40)
    price = models.IntegerField()
    curr_students = models.IntegerField()
    faculty_name = models.CharField(max_length=200)
    faculty_role = models.CharField(max_length=200)
    faculty_img = models.ImageField(upload_to="pics")

    def __str__(self):
        return str(self.name)

class categories(models.Model):
    category = models.CharField(max_length=200)
    des = models.CharField(max_length=40)
    img = models.ImageField(upload_to="pics")
    no_of_courses = models.IntegerField()

    def __str__(self):
        return str(self.category)
    
class teacher(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    number = models.CharField(max_length=10)
    course = models.CharField(max_length=200)
    category = models.CharField(max_length=40)
    course_file = models.FileField(upload_to="")

    def __str__(self):
        return str(self.name)
    
class mycourses(models.Model):
    name = models.CharField(max_length=200)
    mycourse = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)