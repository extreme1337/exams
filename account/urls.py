from django.urls import path, include

from .views import *

app_name = 'account'

urlpatterns = [
    path('students/', include(([
        path('', ExamListView.as_view(), name='exam_list' ),
    ]))),
#    path('teachers/', include(([

#   ]))),
]
