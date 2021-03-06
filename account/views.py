from os import name
from django.http.response import JsonResponse
from django.urls.conf import path
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from school.models import Exam
from django.contrib import messages
from django.contrib.auth import authenticate, login
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
from django.template import RequestContext


# Create your views here.
def custom_page_not_found_view(request, exception):
    return render(request, '404.html', {})

def custom_error_view(request, exception=None):
    return render(request, '500.html', {})

def custom_permissin_denied_view(request, exception=None):
    return render(request, '403.html', {})

def bad_request(request, exception=None):
    return render(request, '400.html', {})


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:exam_change_list')
        elif request.user.is_admin:
            return redirect('admins:dashboard')
        else:
            return redirect('students:exam_list')
    return render(request, 'home.html')

    
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
    student = request.user.student

    if student.exams.filter(pk=pk).exists():
        queryset = request.user.student.taken_exams \
            .select_related('exam', 'exam__subject') \
                .order_by('exam__type')
        return render(request, "students/taken_exam_list.html", {'taken_exams': queryset})
    else:
        return render(request, 'students/exam.html', {'exam': exam})


def exam_data_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    questions = []
    for q in exam.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})

    print(questions)   
    
    return JsonResponse({
        'data': questions,
        'time': exam.duration,
    })


@login_required
@student_required
def save_exam_view(request, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = get_object_or_404(Question, question_text=k)
            questions.append(question)
        print(questions)
        
        student = request.user.student
        exam = get_object_or_404(Exam, pk=pk)

        max_score = 0
        score = 0
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.question_text)
            max_score += q.points
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        StudentAnswer.objects.create(student=student, answer=a)
                        if a.correct:
                            score += q.points
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        multiplier = score / max_score
        print("###################### MAX SCORE")
        print(max_score)
        print("########################## SCORE")
        print(score)
        score_ = multiplier * 100
        print(score_)
        
        TakenExam.objects.create(student=student, exam=exam, score=score_)

        if score_>=exam.required_score_to_pass:
            return JsonResponse({'passed': True, 'score':score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})
    

method_decorator([login_required, student_required], name='dispatch')
class TakenExamsListView(ListView):
    model = TakenExam
    context_object_name = 'taken_exams'
    template_name = 'students/taken_exam_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_exams \
            .select_related('exam', 'exam__subject') \
                .order_by('exam__type')

        return queryset


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
        messages.success(self.request, 'The exam was created with success! Go ahed and add some exams')
        return redirect('teachers:exam_change', exam.pk)



@method_decorator([login_required, teacher_required], name='dispatch')
class ExamTeacherUpdateView(UpdateView):
    model = Exam
    fields = ('type', 'subject', )
    context_object_name = 'exam'
    template_name = 'teachers/exam_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
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
        extra_context = self.get_context_data(**kwargs)
        exam = self.get_object()
        taken_exams = exam.taken_exams.select_related('student__user').order_by('-date')
        total_taken_exams = taken_exams.count()
        exam_score = exam.taken_exams.aggregate(average_score=Avg('score'))
        
        extra_context = {
            'taken_exams': taken_exams,
            'total_taken_exams': total_taken_exams,
            'exam_score': exam_score,
        }
        kwargs.update(extra_context)
        return super().get_context_data()

    def get_queryset(self):
        return self.request.user.exams.all()


@login_required
@teacher_required
def question_add(request, pk):
    exam = get_object_or_404(Exam, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('teachers:exam_change', exam.pk)
        else:
            form = QuestionForm()
    form = QuestionForm()
    return render(request, 'teachers/question_add_form.html', {'exam': exam, 'form': form})


@login_required
@teacher_required
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


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'teachers/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['exam'] = question.exam
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.question_text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(exam__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('teachers:exam_change', kwargs={'pk': question.exam_id})
    


@login_required
@teacher_required
def change_activity(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    exam.active = not exam.active
    exam.save()
    return redirect('teachers:exam_change_list')



method_decorator([login_required, teacher_required], name='dispatch')
class ExamResultsView(DetailView):
    model = Exam
    context_object_name = 'exam'
    template_name = 'teachers/exam_results.html'

    def get_context_data(self, **kwargs):
        exam = self.get_object()
        taken_exams = exam.taken_exams.select_related('student__user').order_by('-date')
        total_taken_exams = taken_exams.count()
        exam_score = exam.taken_exams.aggregate(average_score=Avg('score'))
        extra_content = {
            'taken_exams': taken_exams,
            'total_taken_exams': total_taken_exams,
            'exam_score': exam_score
        }
        kwargs.update(extra_content)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.exams.all()



#####################################################################################
################################ ADMIN VIEWS ########################################
#####################################################################################

@login_required
@admin_required
def dashboard(request):
    return render(request, 'admin/dashboard.html', {})



@login_required
@admin_required
def all_users(request):
    return render(request, 'admin/users.html', {})

@method_decorator([login_required, admin_required], name='dispatch')
class AllStudentsListView(ListView):
    model = User
    ordering = ('last_name', )
    context_object_name = 'students'
    template_name = 'admin/students.html'

    def get_queryset(self):
        queryset = User.objects.filter(is_student=True)
        return queryset

@method_decorator([login_required, admin_required], name='dispatch')
class AllTeachersListView(ListView):
    model = User
    ordering = ('last_name', )
    context_object_name = 'teachers'
    template_name = 'admin/teachers.html'

    def get_queryset(self):
        queryset = User.objects.filter(is_teacher=True)
        return queryset

@method_decorator([login_required, admin_required], name='dispatch')
class AllSubjectsListView(ListView):
    model = Subject
    ordering = ('name', )
    context_object_name = 'subjects'
    template_name = 'admin/subjects.html'

    def get_queryset(self):
        queryset = Subject.objects.all()
        return queryset

@method_decorator([login_required, admin_required], name='dispatch')
class AllSchoolsListView(ListView):
    model = School
    ordering = ('name', )
    context_object_name = 'schools'
    template_name = 'admin/schools.html'

    def get_queryset(self):
        queryset = School.objects.all()
        return queryset

@method_decorator([login_required, admin_required], name='dispatch')
class AllExamsListView(ListView):
    model = Exam
    ordering = ('type', )
    context_object_name = 'exams'
    template_name = 'admin/exams.html'

    def get_queryset(self):
        queryset = Exam.objects.all()
        return queryset

@login_required
@admin_required
def change_activity_admin(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    exam.active = not exam.active
    exam.save()
    return redirect('admins:exams')

@method_decorator([login_required, admin_required], name='dispatch')
class SchoolAdminCreateView(CreateView):
    model = School
    fields = ('name', 'course')
    context_object_name = 'schools'
    template_name = 'admin/add_school.html'

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.save()
        messages.success(self.request, 'New school is successfully added.')
        return redirect('admins:schools')


@method_decorator([login_required, admin_required], name='dispatch')
class SchoolAdminUpdateView(UpdateView):
    model = School
    fields = ('name', 'course', )
    context_object_name = 'school'
    template_name = 'admin/update_school.html'

    def get_success_url(self):
        school = self.get_object()
        return reverse('admins:schools')


@method_decorator([login_required, admin_required], name='dispatch')
class SchoolAdminDeleteView(DeleteView):
    model = School
    context_object_name = 'school'
    template_name = 'admin/school_delete_success.html'


    def get_success_url(self):
        school = self.get_object()
        return reverse('admins:schools')


@method_decorator([login_required, admin_required], name='dispatch')
class SubjectAdminCreateView(CreateView):
    model = Subject
    fields = ('name', 'school')
    context_object_name = 'subject'
    template_name = 'admin/add_subject.html'

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.save()
        messages.success(self.request, 'New subject is successfully added.')
        return redirect('admins:subjects')


@method_decorator([login_required, admin_required], name='dispatch')
class SubjectAdminUpdateView(UpdateView):
    model = Subject
    fields = ('name', 'school', )
    context_object_name = 'subject'
    template_name = 'admin/update_subject.html'

    def get_success_url(self):
        school = self.get_object()
        return reverse('admins:subjects')


@method_decorator([login_required, admin_required], name='dispatch')
class SubjectAdminDeleteView(DeleteView):
    model = Subject
    context_object_name = 'subject'
    template_name = 'admin/subject_delete_success.html'


    def get_success_url(self):
        school = self.get_object()
        return reverse('admins:subjects')


@method_decorator([login_required, admin_required], name='dispatch')
class AddNewUserView(CreateView):  
    model = User
    form_class = AdminUserForm
    context_object_name = 'user'
    template_name = 'admin/add_new_user.html'


    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        if user.is_student:
            Student.objects.create(user=user)
        messages.success(self.request, 'New user is successfully added.')
        return redirect('admins:users')


@method_decorator([login_required, admin_required], name='dispatch')
class UserAdminDeleteView(DeleteView):
    model = User
    context_object_name = 'user'
    template_name = 'admin/user_delete_success.html'
    


    def get_success_url(self):
        school = self.get_object()
        return reverse('admins:users')

@method_decorator([login_required, admin_required], name='dispatch')
class UpdateUserView(UpdateView):
    model = User
    form_class = AdminUserForm
    context_object_name = 'user'
    template_name = 'admin/edit_user.html'


    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        if user.is_student:
            Student.objects.get_or_create(user=user)
        messages.success(self.request, f'User is successfully updated. {user.username}')
        return redirect('admins:users')

    def get_success_url(self):
        school = self.get_object()
        return reverse('admins:users')

@method_decorator([login_required, teacher_required, student_required], name='dispatch')
class UpdateUserDetailsView(UpdateView):
    model = User
    form_class = UserForm
    context_object_name = 'user'
    template_name = 'user/profile.html'


    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        if user.is_student:
            Student.objects.get_or_create(user=user)
        messages.success(self.request, f'User is successfully updated. {user.username}')
        return redirect('home')

    def get_success_url(self):
        school = self.get_object()
        return reverse('home')



@method_decorator([login_required, admin_required], name='dispatch')
class ExamAdminCreateView(CreateView):
    model = Exam
    form_class = AddExamAdminForm
    context_object_name = 'exams'
    template_name = 'admin/exam_add_form.html'

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.save()
        messages.success(self.request, 'The exam was created with success! Go ahed and add some exams')
        return redirect('admins:exam_change_admin', exam.pk)


@method_decorator([login_required, admin_required], name='dispatch')
class ExamAdminDeleteView(DeleteView):
    model = Exam
    context_object_name = 'exam'
    template_name = 'admin/exam_delete_confirm_confirm.html'
    success_url = reverse_lazy('admins:exam_change_list')

    def delete(self, request, *args, **kwargs):
        exam = self.get_object()
        messages.success(request, 'The exam %s was deleted with success!' % exam.type)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.exams.all()

@method_decorator([login_required, admin_required], name="dispatch")
class ExamAdminUpdateView(UpdateView):
    model = Exam
    fields = ('type', 'subject', )
    context_object_name = 'exam'
    template_name = 'admin/exam_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)


    def get_success_url(self):
        return reverse('admins:exam_change_admin', kwargs={'pk': self.object.pk})


@login_required
@admin_required
def change_activity_exam_admin(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    exam.active = not exam.active
    exam.save()
    return redirect('admins:exams')


@login_required
@admin_required
def question_add_admin(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('admins:exam_change_admin', exam.pk)
        else:
            form = QuestionForm()
    form = QuestionForm()
    return render(request, 'admin/question_add_form.html', {'exam': exam, 'form': form})


@login_required
@admin_required
def question_change_admin(request, exam_pk, question_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
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
            return redirect('admins:exam_change_admin', exam.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'admin/question_change_form_admin.html', {
        'exam': exam,
        'question': question,
        'form': form,
        'formset': formset
    })


@method_decorator([login_required, admin_required], name='dispatch')
class QuestionAdminDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'admin/question_delete_confirm_admin.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['exam'] = question.exam
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.question_text)
        return super().delete(request, *args, **kwargs)


    def get_success_url(self):
        question = self.get_object()
        return reverse('admins:exam_change_admin', kwargs={'pk': question.exam_id})

