from django.urls import path
from . import views, apis

app_name = 'website'

urlpatterns = [
    path('signin/', views.signin, name='signin')
    # path('signin/', apis.SigninUserAPI.as_view(), name='signin'),
]