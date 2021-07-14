from django.contrib import admin
from .models import Score
# Register your models here.
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'score']

admin.site.register(Score, ScoreAdmin)
