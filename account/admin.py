from django.contrib import admin
from .models import *

# Register your models here.
class StudentInline(admin.TabularInline):
    model = Student


class UserStudentAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']
    inlines = [StudentInline]
    #exclude = ['Student.taken_exams']
    #readonly_fields=('Student.taken_exams', )



admin.site.register(User, UserStudentAdmin)





