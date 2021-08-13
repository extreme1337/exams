from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.expressions import F
from django.utils.translation import gettext_lazy as _
from school.models import Answer, Exam, Question, School, Subject

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_image():
    return 'images/logo_1080_1080.png'

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=220)
    last_name = models.CharField(max_length=220)
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True
    )
    username = models.CharField(max_length=40, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    proflie_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_profile_image_name(self):
        return str(self.proflie_image)[str(self.proflie_image).index(f'profile_images/{self.pk}/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    


class Student(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True, related_name='student')
    exams = models.ManyToManyField(Exam, through='TakenExam')

    def get_unanswered_questions(self, exam):
        answered_questions = self.exam_answers \
            .filter(answer__question__exam=exam) \
            .values_list('answer__question__pk', flat=True)
        questions = exam.questions.exclude(pk__in=answered_questions).order_by('type')
        return questions

    def __str__(self):
        return self.user.username


class TakenExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_exams')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='taken_exams')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.exam.type

class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_answeres')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer')

    def __str__(self):
        return self.answer.text
    
