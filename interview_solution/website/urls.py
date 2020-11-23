from django.urls import path
from django.conf.urls import url
from . import views, apis, schoolInfo

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
    path('findID/<int:student>', views.findID, name='findID'),
    path('findPW/<int:student>', views.findPW, name='findPW'),
    path('resultPW/<int:student>/<userID>/', views.resultPW, name='resultPW'),
    path('teacher/studentVideo/<int:reportID>', views.teacherVideo, name='teacherVideo'),
    path('teacher/questionSend/<studentID>', views.questionSend, name='questionSend'),
    path('teacher/questionSend/delete/<int:questionID>', views.questionSendDelete, name='questionSendDelete'),
    path('teacher/studentVideo/edit1/<int:reportID>', views.commentEdit1, name="commentEdit1"),
    path('teacher/studentVideo/edit2/<int:reportID>', views.commentEdit2, name="commentEdit2"),
    path('teacher/studentVideo/edit3/<int:reportID>', views.commentEdit3, name="commentEdit3"),
    path('teacher/studentVideo/delete1/<int:reportID>', views.commentDelete1, name="commentDelete1"),
    path('teacher/studentVideo/delete2/<int:reportID>', views.commentDelete2, name="commentDelete2"),
    path('teacher/studentVideo/delete3/<int:reportID>', views.commentDelete3, name="commentDelete3"),
]
