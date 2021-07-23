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
    fields = ('type', 'subject', 'active', 'duration', 'required_score_to_pass', 'nuber_of_questions', )
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
        kwargs['questions'] = self.get_object().questions
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


def question_add(request, pk):

    exam = get_object_or_404(Exam, pk=pk, owner=request.user)
    print("BEFORE IF REQUEST ##################3")
    if request.method == 'POST':
        print("#################### AFTER PRINT REQUEST")
        form = QuestionForm(request.POST)
        print("########BEFORE FORM#############")
        if form.is_valid():
            print("*****************IN FORM***************")
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('teachers:exam_change', exam.pk, question.pk)
        else:
            print("**********###############************")
            form = QuestionForm()
    form = QuestionForm()
    return render(request, 'teachers/question_add_form.html', {'exam': exam, 'form': form})


def question_change(request, exam_pk, question_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `exam` and
    # `question` we are making sure only the owner of the exam can
    # change its details and also only questions that belongs to this
    # specific exam can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    exam = get_object_or_404(Exam, pk=exam_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, exam=exam)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('teachers:exam_change', exam.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'teachers/question_change_form.html', {
        'exam': exam,
        'question': question,
        'form': form,
        'formset': formset
    })