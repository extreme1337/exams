from django.contrib import admin
from .models import *

# Register your models here.
class UserStudentAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'date_joined', 'last_login', 'student', 'first_name', 'last_name']
    search_fields = ['email', 'username']
    readonly_fields = ['id', 'date_joined', 'last_login']



admin.site.register(User, UserStudentAdmin)


class UserTakenExam(admin.ModelAdmin):
    list_display = "__all__"

admin.site.register(TakenExam)
admin.site.register(StudentAnswer)

admin.site.register(Student)





