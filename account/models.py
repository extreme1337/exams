from django.db import models
from django.utils.translation import gettext_lazy as _
from school.models import Exam, School, Subject

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=220)
    last_name = models.CharField(max_length=220)
    email = models.EmailField()
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    taken_exams = models.ManyToManyField(Exam, related_name='taken_exams', blank=True, null=True)



class Admin(models.Model):
    pass

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    
