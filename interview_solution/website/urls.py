<<<<<<< HEAD
from django.urls import path

app_name = 'website'

urlpatterns = []

from django.conf.urls import url
from . import views
from . import views, apis

app_name = 'website'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    url(r'^ajax/tag/autocomplete/$',views.ajax_schoolInfo_autocomplete),
    path('student/signin/', views.studentSignin, name='studentSignin'),
    # path('signin/', apis.SigninUserAPI.as_view(), name='signin'),
    path('teacher/signin/', views.teacherSignin, name='teacherSignin')
]
=======
from django.urls import path
from django.conf.urls import url
from . import views, apis

app_name = 'website'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    url(r'^ajax/tag/autocomplete/$',views.ajax_schoolInfo_autocomplete),
    path('student/signin/', views.studentSignin, name='studentSignin'),
    path('student/signoff', views.studentSignoff, name='studentSignoff'),
    # path('signin/', apis.SigninUserAPI.as_view(), name='signin'),
    path('teacher/signin/', views.teacherSignin, name='teacherSignin'),
    path('teacher/signoff', views.teacherSignoff, name='teacherSignoff'),
    path('findID/', views.findID, name='findID'),
    path('findPW/', views.findPW, name='findPW'),
    path('resultPW/<userID>/', views.resultPW, name='resultPW'),
    path('', views.intro, name='intro'),
    path('student/home', views.studentHome, name='studentHome'),
    # path('teacher/home', views.teacherHome, name='teacherHome'),
]
>>>>>>> cb5195591566723db54cfc312433fc8d04b1d30e
