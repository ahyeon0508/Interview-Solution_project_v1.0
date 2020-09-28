from django.urls import path
from . import views, apis

app_name = 'website'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    # path('signin/', apis.SigninUserAPI.as_view(), name='signin'),
    path('findID/', views.findID, name='findID'),
    path('findPW/', views.findPW, name='findPW'),
    path('resultPW/', views.resultPW, name='resultPW'),
]