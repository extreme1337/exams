from django.urls import path, include

from .views import *


urlpatterns = [
    path('students/', include(([
        path('',  ExamStudentListView.as_view(), name='exam_list'),
        path('exam/<int:pk>/', take_exam, name='take_exam'),
    ], 'account'), namespace='students')),
    path('teachers/', include(([
        path('', ExamTeacherListView.as_view(), name='exam_change_list'),
        path('exam/add/', ExamTeacherCreateView.as_view(), name='exam_add'),
        path('exam/<int:pk>/', ExamTeacherUpdateView.as_view(), name='exam_change'),
    ], 'account'), namespace='teachers'))

]
