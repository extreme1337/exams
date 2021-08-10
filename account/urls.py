from os import name
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *


urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('', home, name='home'),
    path('students/', include(([
        path('',  ExamStudentListView.as_view(), name='exam_list'),
        path('exam/<int:pk>/', exam_view, name='take_exam'),
        path('exam/<pk>/data/', exam_data_view, name='exam_data_view'),
        path('exam/<pk>/save/', save_exam_view, name='save_exam'),
        path('exam/taken/', TakenExamsListView.as_view(), name='taken_exam_list'),
    ], 'account'), namespace='students')),
    path('teachers/', include(([
        path('', ExamTeacherListView.as_view(), name='exam_change_list'),
        path('exam/add/', ExamTeacherCreateView.as_view(), name='exam_add'),
        path('exam/<int:pk>/', ExamTeacherUpdateView.as_view(), name='exam_change'),
        path('exam/<int:pk>/activity/', change_activity, name='exam_change_activity'),
        path('exam/<int:pk>/delete/', ExamTeacherDeleteView.as_view(), name='exam_delete'),
        path('exam/<int:pk>/question/add/', question_add, name='question_add'),
        path('exam/<int:exam_pk>/question/<int:question_pk>/', question_change, name='question_change'),
        path('exam/<int:exam_pk>/question/<int:question_pk>/delete', QuestionDeleteView.as_view(), name='question_delete'),
        path('exam/<int:pk>/results/', ExamResultsView.as_view(), name='exam_results'),
    ], 'account'), namespace='teachers'))

]
