from django.db import models
from django.db.models.deletion import CASCADE
from school.models import Exam

# Create your models here.
class Score(models.Model):
    user = models.CharField(max_length=220)
    score = models.FloatField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.exam} (score: {self.score})"