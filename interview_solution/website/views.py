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

def findID(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        phone = request.POST.get('phone', '')

        try:
            user = User.objects.filter(username=username, phone=phone)
            if user is not None:
                return render(request, 'resultID.html', {'userID':user.username})
            else:
                return render(request, 'findID.html', {'error': 'username or phone is incorrect'})
        except:
            return render(request, 'findID.html', {'error': 'username or phone is incorrect'})
    else:
        return render(request, 'findID.html')

def findPW(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        userID = request.POST.get('userID', '')
        phone = request.POST.get('phone', '')

        try:
            user = User.objects.filter(username=username, userID=userID, phone=phone)
            if user is not None:
                return redirect(reverse('website:resultPW', args=[str(userID)]))
            else:
                return render(request, 'findPW.html', {'error': 'username or userID or phone is incorrect'})
        except:
            return render(request, 'findPW.html', {'error': 'username or userID or phone is incorrect'})
    else:
        return render(request, 'findPW.html')

def resultPW(request, userID):
    if request.method == "POST":
        password = request.POST.get('password', '')
        passwordChk = request.POST.get('passwordChk', '')

        try:
            if password == passwordChk:
                user = User.objects.get(userID=userID)
                user.set_password(password)
                user.save()
                return redirect(reverse('website:signin'))
            else:
                return render(request, 'resultPW.html', {'error': 'password incorrect'})
        except:
            return render(request, 'resultPW.html', {'error': 'password incorrect'})
    else:
        return render(request, 'resultPW.html')