from django.contrib import admin
from .models import *

# Register your models here.
class UserStudentAdmin(admin.ModelAdmin):
    list_display = ['username', 'student', 'first_name', 'last_name']



admin.site.register(User, UserStudentAdmin)


class UserTakenExam(admin.ModelAdmin):
    list_display = "__all__"

admin.site.register(TakenExam)

admin.site.register(Student)





