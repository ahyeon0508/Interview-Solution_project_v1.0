from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User

@csrf_exempt
def signin(request):
    if request.method == "POST":
        userID = request.POST.get('userID', '')
        password = request.POST.get('password', '')

        try:
            user = User.objects.get(userID=userID)
            if check_password(password, user.password):
                return render(request, 'signin.html', {'error' : '성공'})
            else:
                return render(request,'signin.html',{'error':'username or password is incorrect'})
        except:
            return render(request, 'signin.html', {'error': 'username or password is incorrect'})
    else:
        return render(request,'signin.html')

@login_required
def mypage(request):
    user = request.user
    if user:
        return render(request,'mypage.html',{'user': user})
    else:
        return render(request,'login.html')