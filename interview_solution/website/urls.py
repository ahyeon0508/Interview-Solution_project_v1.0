from django.urls import path
from . import views, apis, schoolInfo
from django.conf.urls import url

app_name = 'website'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('schooldb/',schoolInfo.schoolInfo_db,name='schoolInfo'),
    url(r'^signup/search/$',views.ajax_schoolInfo_autocomplete, name='search_signup'),
    path('student/signin/', views.studentSignin, name='studentSignin'),
    # path('signin/', apis.SigninUserAPI.as_view(), name='signin'),
    path('teacher/signin/', views.teacherSignin, name='teacherSignin')
]
