from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('signup/', views.SignupUserAPI.as_view(), name='signup'),
    path('signin/', views.SigninUserAPI.as_view(), name='signin'),
]