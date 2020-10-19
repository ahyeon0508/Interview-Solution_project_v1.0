from django.urls import path
from django.conf.urls import url
from . import views, apis, schoolInfo, questionDB

app_name = 'website'

urlpatterns = [
    path('student/signup/', views.studentSignup, name='studentSignup'),
    path('teacher/signup/', views.teacherSignup, name='teacherSignup'),
    path('schooldb/',schoolInfo.schoolInfo_db,name='schoolInfo'),
    url(r'^student/signup/search/$',views.ajax_schoolInfo_autocomplete, name='search_signup'),
    url(r'^teacher/signup/search/$',views.ajax_schoolInfo_autocomplete, name='search_signup'),
    path('student/signup/checkid',views.studentcheckID,name='studentCheckid'),
    path('teacher/signup/checkid',views.teachercheckID,name='teacherCheckid'),
    path('student/signin/', views.studentSignin, name='studentSignin'),
    # path('signin/', apis.SigninUserAPI.as_view(), name='signin'),
    path('teacher/signin/', views.teacherSignin, name='teacherSignin'),
    path('findID/', views.findID, name='findID'),
    path('findPW/', views.findPW, name='findPW'),
    path('resultPW/<userID>/', views.resultPW, name='resultPW'),
    path('questionDB/',questionDB.db,name='questionDB'),
]
