from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import fields
from django.forms.utils import ValidationError

from school.models import *
from .models import *

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', )


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

