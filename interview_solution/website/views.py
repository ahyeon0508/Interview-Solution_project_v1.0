from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from requests import auth

from .models import User, Teacher

@csrf_exempt
def studentSignin(request):
    if request.method == "POST":
        userID = request.POST.get('userID', '')
        password = request.POST.get('password', '')

        try:
            user = User.objects.get(userID=userID)
            if check_password(password, user.password):
                request.session['user'] = user.userID
                return render(request, 'signin.html', {'error' : '성공'})
            else:
                return render(request,'signin.html',{'error':'username or password is incorrect'})
        except:
            return render(request, 'signin.html', {'error': 'username or password is incorrect'})
    else:
        return render(request,'signin.html')

def teacherSignin(request):
    if request.method == "POST":
        userID = request.POST.get('userID', '')
        password = request.POST.get('password', '')

        try:
            user = Teacher.objects.get(userID=userID)
            if check_password(password, user.password):
                request.session['user'] = user.userID
                return render(request, 'signin.html', {'error' : '성공'})
            else:
                return render(request,'signin.html',{'error':'username or password is incorrect'})
        except:
            return render(request, 'signin.html', {'error': 'username or password is incorrect'})
    else:
        return render(request,'signin.html')

@login_required
def mypage(request):
    if request.method == "POST":
        user = request.user
        question = request.POST.get('findQuestion', '')
        answer = request.POST.get('findAnswer', '')
        oldPW = request.POST.get('password', '')
        newPW = request.POST.get('passwordChk', '')
        phone = request.POST.get('phone', '')
        school = request.POST.get('schoolName', '')
        grade = request.POST.get('grade', '')
        if check_password(oldPW, user.password) is False or phone != user.phone or question != user.question or answer != user.answer or school != user.school or grade != user.grade:
            return render(request, 'mypage_Info.html', {'error': '입력한 기존 정보가 잘못되었습니다.'})
        else:
            user.set_password(newPW)
            user.save()
            request.session['user'] = user.userID
            return render(request, 'mypage_Info.html', {'notice': '수정이 완료되었습니다.'})
    else:
        user = User.objects.get(userID=request.user.userID)
        return render(request, 'mypage_Info.html', {'user':user})