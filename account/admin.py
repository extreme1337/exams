from django.contrib import admin
from .models import *

# Register your models here.
class UserStudentAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']



admin.site.register(User, UserStudentAdmin)





