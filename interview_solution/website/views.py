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

def findIDPW(request):
    if request.method == "POST":
        userID = request.POST.get('userID', '')
        phone = request.POST.get('phone', '')

        try:
            user = User.objects.filter(userID=userID, phone=phone)
            if user is not None:
                return render(request, 'resultIDPW.html', {'userID':user.userID, 'password':user.password})
            else:
                return render(request, 'findIDPW.html', {'error': 'username or password is incorrect'})
        except:
            return render(request, 'findIDPW.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'findIDPW.html')