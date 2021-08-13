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
    ], 'account'), namespace='teachers')),

    path('admins/', include(([
        path('',  dashboard, name='dashboard'),
        path('users/',  all_users, name='users'),
        path('users/students/',  AllStudentsListView.as_view(), name='students'),
        path('users/teachers/',  AllTeachersListView.as_view(), name='teachers'),
        path('subjects/',  AllSubjectsListView.as_view(), name='subjects'),
        path('schools/',  AllSchoolsListView.as_view(), name='schools'),
        path('exams/',  AllExamsListView.as_view(), name='exams'),
        path('exams/<int:pk>/activity/', change_activity_admin, name='exam_change_admin'),
        path('schools/add_new_school/', SchoolAdminCreateView.as_view(), name='add_school'),
        path('schools/update_school/<int:pk>', SchoolAdminUpdateView.as_view(), name='update_school'),
        path('schools/delete_school/<int:pk>', SchoolAdminDeleteView.as_view(), name='delete_school'),
        path('schools/add_new_subject/', SubjectAdminCreateView.as_view(), name='add_subject'),
        path('schools/update_subject/<int:pk>', SubjectAdminUpdateView.as_view(), name='update_subject'),
        path('schools/delete_subject/<int:pk>', SubjectAdminDeleteView.as_view(), name='delete_subject'),
        
    ], 'account'), namespace='admins')),
    

]
