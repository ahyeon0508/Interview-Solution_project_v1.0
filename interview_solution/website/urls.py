from django.urls import path
from . import views, apis

app_name = 'website'

urlpatterns = [
    path('student/signin/', views.studentSignin, name='signin'),
    # path('signin/', apis.SigninUserAPI.as_view(), name='signin'),
    path('teacher/signin/', views.teacherSignin, name='signin')
]