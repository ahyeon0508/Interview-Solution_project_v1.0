from django.urls import path
<<<<<<< HEAD

app_name = 'website'

urlpatterns = []
=======
from django.conf.urls import url
from . import views

app_name = 'website'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    url(r'^ajax/tag/autocomplete/$',views.ajax_schoolInfo_autocomplete),
]
>>>>>>> b0d5b4f047c064311ce0b9f39928954458247a41
