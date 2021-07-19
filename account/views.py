from school.models import Exam
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

# Create your views here.
#@method_decorator([login_required], name='dispatch')
class ExamListView(ListView):
    model = Exam
    context_object_name = 'exams'
    template_name = 'students/exams.html'

    def get_queryset(self):
        queryset = Exam.objects.filter(active=True)
        return queryset
