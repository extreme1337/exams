from django.db import models
from django.utils.translation import gettext_lazy as _



# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=220)
    course = models.CharField(max_length=220)

    def __str__(self):
        return f"{self.name}: {self.course}"

class Subject(models.Model):
    name = models.CharField(max_length=220)
    school = models.ManyToManyField(School)
    
    def __str__(self):
        return self.name

class Exam(models.Model):
    type = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    duration = models.IntegerField()
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    subject  = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject}: {self.type}"


class Question(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'EA', _('Easy')
        NORMAL = 'NO', _('Normal')
        HARD = 'HA', _('Hard')
    question_text = models.CharField(max_length=250)
    picture = models.ImageField(null=True, blank=True)
    level = models.CharField(max_length=6, choices=Difficulty.choices)
    multiple_answares = models.BooleanField(default=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return self.question_text


class Answare(models.Model):
    text = models.CharField(max_length=300)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


