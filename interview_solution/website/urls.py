from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'website'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    url(r'^ajax/tag/autocomplete/$',views.ajax_schoolInfo_autocomplete),
]