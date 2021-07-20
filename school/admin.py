from django.contrib import admin
from .models import Answer, Exam, Question, School, Subject

# Register your models here.
class ExamAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__', 'active')
  
    def active(self, obj):
        return obj.is_active == 1
  
    active.boolean = True

class AnswerInline(admin.TabularInline):
    model = Answer
  

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(School)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['__str__']
admin.site.register(Subject, SubjectAdmin)
