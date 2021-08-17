from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import fields, widgets
from django.forms.utils import ValidationError

from school.models import *
from .models import *

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'picture', 'level', 'multiple_answers', 'points')
        

class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer=False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('correct', False):
                    has_one_correct_answer=True
                    break
        if has_one_correct_answer == False:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeExamForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None
    )

    class Meta:
        models = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('question_text')


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'proflie_image', 'email', 'username', 'password', 'is_student', 'is_teacher', 'is_admin',)
    
        widgets = {
            'password': widgets.TextInput(attrs={'type': 'password',})
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'proflie_image', 'email', 'username', 'password', )

        widgets = {
            'password': widgets.TextInput(attrs={'type': 'password',})
        }

class AddExamAdminForm(forms.ModelForm):
    teachers = User.objects.filter(is_teacher=True)
    owner = forms.ModelChoiceField(queryset=teachers)
    class Meta:
        model = Exam
        fields = ('type', 'subject', 'active', 'duration', 'required_score_to_pass', 'nuber_of_questions', 'owner', )