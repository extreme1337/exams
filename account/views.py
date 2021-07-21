from django.http.response import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
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


'''method_decorator([student_required, login_required]) 
def take_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    student = request.user
    print(student)    
    
    if student.exams.filter(pk=pk).exists():
        return render(request, '')


    total_questions = exam.questions.count()
    unaswered_questions = student.get_unanswered_questions(exam)
    total_unaswered_questions = unaswered_questions.count()
    progress = 100 - round(((total_unaswered_questions - 1) / total_questions) * 100)
    question = unaswered_questions.first()


    if request.method == 'POST':
        form = TakeExamForm(question=question, data=request.POST)
        
    

    return render(request, 'students/exam.html')'''



method_decorator([login_required, student_required], name='dispatch')
def exam_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'students/exam.html', {'exam': exam})


def exam_data_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    questions = []
    for q in exam.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': exam.duration,
    })



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


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamTeacherDeleteView(DeleteView):
    model = Exam
    context_object_name = 'exam'
    template_name = 'teachers/exam_delete_confirm.html'
    success_url = reverse_lazy('teachers:exam_change_list')

    def delete(self, request, *args, **kwargs):
        exam = self.get_object()
        messages.success(request, 'The exam %s was deleted with success!' % exam.type)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.exams.all()


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamResultsView(DetailView):
    model = Exam
    context_object_name = 'exam'
    template_engine = 'teachers/exam_results.html'

    def get_context_data(self, **kwargs):
        exam = self.get_object()
        taken_exams = exam.taken_exams.select_related('student__user').order_by('-date')
        total_taken_exams = taken_exams.count()
        exam_score = exam.taken_exams.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_exams': taken_exams,
            'total_taken_exams': total_taken_exams,
            'exam_score': exam_score
        }
        kwargs.update(extra_context)
        return super().get_context_data()

    def get_queryset(self):
        return self.request.user.exams.all()

