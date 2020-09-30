from django.urls import path
app_name = 'website'

urlpatterns = []
from . import views, apis

app_name = 'website'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    # path('signin/', apis.SigninUserAPI.as_view(), name='signin'),
    path('mypage/', views.mypage, name='mypage'),
]
