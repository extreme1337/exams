from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from school.models import Answare, Exam, School, Subject

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=220)
    last_name = models.CharField(max_length=220)
    email = models.EmailField()
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    exams = models.ManyToManyField(Exam, through='TakenExam')

    def get_unanswered_questions(self, exam):
        answered_questions = self.exam_answares \
            .filter(answare__question__exam=exam) \
            .values_list('answare__question__pk', flat=True)
        questions = exam.questions.exclude(pk__in=answered_questions).order_by('type')
        return questions

    def __str__(self):
        return self.user.username

class Admin(models.Model):
    pass

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class TakenExam(models.Model):
    studen = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_exams')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='taken_exams')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answeres')
    answer = models.ForeignKey(Answare, on_delete=models.CASCADE, related_name='+')
    
