from django.urls import path
<<<<<<< HEAD

app_name = 'website'

urlpatterns = []
=======
from . import views, apis

app_name = 'website'

urlpatterns = [
    path('signin/', views.signin, name='signin')
    # path('signin/', apis.SigninUserAPI.as_view(), name='signin'),
]
>>>>>>> b980a489352d40603aef40585dcf40e1bcb18854
