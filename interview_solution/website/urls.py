from django.urls import path
from django.conf.urls import url
from . import views, apis

app_name = 'website'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    url(r'^ajax/tag/autocomplete/$',views.ajax_schoolInfo_autocomplete),
    path('student/signin/', views.studentSignin, name='studentSignin'),
    # path('signin/', apis.SigninUserAPI.as_view(), name='signin'),
    path('teacher/signin/', views.teacherSignin, name='teacherSignin'),
    path('findID/', views.findID, name='findID'),
    path('findPW/', views.findPW, name='findPW'),
    path('resultPW/<userID>/', views.resultPW, name='resultPW'),
]
