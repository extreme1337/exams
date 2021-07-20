from school.models import Exam
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from .forms import *
from .decorators import *


# Create your views here.

##########################################################################
##########################STUDENT VIEWS###################################
##########################################################################
@method_decorator([login_required, student_required], name='dispatch')
class ExamStudentListView(ListView):
    model = Exam
    context_object_name = 'exams'
    template_name = 'students/exams.html'

    def get_queryset(self):
        queryset = Exam.objects.filter(active=True)
        return queryset


method_decorator([student_required, login_required]) 
def take_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    student = request.user
    print(student)    
    '''
    if student.exams.filter(pk=pk).exists():
        return render(request, '')


    total_questions = exam.questions.count()
    unaswered_questions = student.get_unanswered_questions(exam)
    total_unaswered_questions = unaswered_questions.count()
    progress = 100 - round(((total_unaswered_questions - 1) / total_questions) * 100)
    question = unaswered_questions.first()


    if request.method == 'POST':
        form = TakeExamForm(question=question, data=request.POST)
    '''    
    

    return render(request, 'students/exam.html')



############################################################################
#############################TEACHER VIEWS##################################
############################################################################
@method_decorator([login_required, teacher_required], name='dispatch')
class ExamTeacherListView(ListView):
    model = Exam
    ordering = ('type', )
    context_object_name = 'exams'
    template_name = 'teachers/exam_change_list.html'

    def get_queryset(self):
        queryset = Exam.objects.filter(owner=self.request.user)#self.request.user.exams \
            #.select_related('subject') \
                #.annotate(question_count=Count('questions', distinct=True)) \
                    #.annotate(taken_count=Count('taken_exams', distinct=True))
        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamTeacherCreateView(CreateView):
    model = Exam
    fields = ('type', 'subject', )
    context_object_name = 'exams'
    template_name = 'teachers/exam_add_form.html'

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.owner = self.request.user
        exam.save()
        messages.success(self.request, 'The exam was created with success! Go aged and add some exams')
        return redirect('teachers:exam_change', exam.pk)



@method_decorator([login_required, teacher_required], name='dispatch')
class ExamTeacherUpdateView(UpdateView):
    model = Exam
    fields = ('type', 'subject', )
    context_object_name = 'exam'
    template_name = 'teachers/exam_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission managment
        This view will only mathc the ids of existing exams that belongs
        to the logged in user
        '''
        return self.request.user.exams.all()

    def get_success_url(self):
        return reverse('teachers:exam_change', kwargs={'pk': self.object.pk})
