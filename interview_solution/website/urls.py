from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views, apis, schoolInfo, questionDB

app_name = 'website'

urlpatterns = [
    path('', views.intro, name='intro'),
    path('student/', views.studentHome, name='studentHome'),
    path('teacher/', views.teacherHome, name='teacherHome'),
    path('student/signup/', views.studentSignup, name='studentSignup'),
    path('teacher/signup/', views.teacherSignup, name='teacherSignup'),
    path('schooldb/',schoolInfo.schoolInfo_db,name='schoolInfo'),
    url(r'^student/signup/search/$',views.ajax_schoolInfo_autocomplete, name='search_signup'),
    url(r'^teacher/signup/search/$',views.ajax_schoolInfo_autocomplete, name='search_signup'),
    path('student/signup/checkid',views.studentcheckID,name='studentCheckid'),
    path('teacher/signup/checkid',views.teachercheckID,name='teacherCheckid'),
    path('student/signin/', views.studentSignin, name='studentSignin'),
    path('teacher/signin/', views.teacherSignin, name='teacherSignin'),
    path('signoff/', views.signoff, name='signoff'),
    path('findID/<int:student>', views.findID, name='findID'),
    path('findPW/<int:student>', views.findPW, name='findPW'),
    path('resultPW/<int:student>/<userID>/', views.resultPW, name='resultPW'),
    path('questionDB/',questionDB.db,name='questionDB'),
    path('student/interview/',views.inter_setting,name='interviewSetting'),
    path('student/interview/q1/<reportID>',views.interview_q1,name='interviewQ1'),
    path('student/interview/q1/record/',views.recordVideo,name='recordVideoQ1'),
    path('student/interview/q1/record_stop/',views.stop_button_q1,name='stopVideoQ1'),
    path('student/interview/q2/<reportID>',views.interview_q2,name='interviewQ2'),
    path('student/interview/q2/record/',views.recordVideo,name='recordVideoQ2'),
    path('student/interview/q2/record_stop/',views.stop_button_q1,name='stopVideoQ2'),
    path('student/interview/q3/<reportID>',views.interview_q3,name='interviewQ3'),
    path('student/interview/q3/record/',views.recordVideo,name='recordVideoQ3'),
    path('student/interview/q3/record_stop/',views.stop_button_q1,name='stopVideoQ3'),
    path('wait/<reportID>', views.wait, name='wait'),
    path('wait/ajax/', views.waitAjax, name='waitAjax'),
    path('waitVideo1/<int:reportID>', views.waitVideo1, name='waitVideo1'),
    path('waitVideo2/<int:reportID>', views.waitVideo2, name='waitVideo2'),
    path('waitVideo3/<int:reportID>', views.waitVideo3, name='waitVideo3'),
    path('myVideo/', views.myVideo, name='myVideo'),
    path('myVideo/ajax/', views.myVideoAjax, name='myVideoAjax'),
    path('myVideo/detail/<int:reportID>', views.myVideoDetail, name='myVideoDetail'),
    path('classVideo/', views.classVideo, name='classVideo'),
    path('classVideo/detail/<int:reportID>', views.classVideoDetail, name='classVideoDetail'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
