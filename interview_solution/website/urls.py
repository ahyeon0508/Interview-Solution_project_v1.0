from django.urls import path
from django.conf.urls import url
from . import views, schoolInfo

app_name = 'website'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('schooldb/',schoolInfo.schoolInfo_db,name='schoolInfo'),
    url(r'^signup/search/$',views.ajax_schoolInfo_autocomplete, name='search_signup'),
]