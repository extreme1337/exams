from django.urls import path, include

from .views import *


urlpatterns = [
    path('students/', include(([
        path('',  ExamStudentListView.as_view(), name='exam_list'),
        path('exam/<int:pk>/', exam_view, name='take_exam'),
        path('exam/<pk>/data/', exam_data_view, name='exam_data_view'),
    ], 'account'), namespace='students')),
    path('teachers/', include(([
        path('', ExamTeacherListView.as_view(), name='exam_change_list'),
        path('exam/add/', ExamTeacherCreateView.as_view(), name='exam_add'),
        path('exam/<int:pk>/', ExamTeacherUpdateView.as_view(), name='exam_change'),
        path('exam/<int:pk>/delete/', ExamTeacherDeleteView.as_view(), name='exam_delete'),
        path('exam/<int:pk>/question/add/', question_add, name='question_add'),
        path('exam/<int:exam_pk>/question/<int:question_pk>/', question_change, name='question_change'),
        path('exam/<int:exam_pk>/question/<int:question_pk>/delete', QuestionDeleteView.as_view(), name='question_delete'),
    ], 'account'), namespace='teachers'))

]
