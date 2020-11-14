from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views, schoolInfo, questionDB

app_name = 'website'

urlpatterns = [
    path('student/signup/', views.studentSignup, name='studentSignup'),
    path('schooldb/',schoolInfo.schoolInfo_db,name='schoolInfo'),
    url(r'^student/signup/search/$',views.ajax_schoolInfo_autocomplete, name='search_signup'),
    path('student/signup/checkid',views.studentcheckID,name='studentCheckid'),
    path('student/signin/', views.studentSignin, name='studentSignin'),
    path('findID/', views.findID, name='findID'),
    path('findPW/', views.findPW, name='findPW'),
    path('resultPW/<userID>/', views.resultPW, name='resultPW'),
    path('questionDB/',questionDB.db,name='questionDB'),
    path('student/interview/',views.inter_setting,name='interviewSetting'),
    path('student/interview/q1/<reportID>',views.interview_q1,name='interviewQ1'),
    path('student/interview/q1/record/',views.recordVideo,name='recordVideoQ1'),
    path('student/interview/q1/record_stop/',views.stop_button_q1,name='stopVideoQ1'),
    path('wait/<reportID>', views.wait, name='wait'),
    path('waitVideo1/', views.waitVideo1, name='waitVideo1'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
