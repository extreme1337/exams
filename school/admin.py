from django.contrib import admin
from .models import Answare, Exam, Question, School, Subject

# Register your models here.
class ExamAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'active')
  
    def active(self, obj):
        return obj.is_active == 1
  
    active.boolean = True

class AnswareInline(admin.TabularInline):
    model = Answare
  

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswareInline]

admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(School)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['__str__']
admin.site.register(Subject, SubjectAdmin)
