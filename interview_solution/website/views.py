from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import User, Teacher, SchoolInfo, Report, StudentQuestion, Question
import json
import logging

@csrf_exempt
def studentSignup(request):
    if request.method == "POST":
        userID = request.POST['userID']
        username = request.POST.get('username','')
        password = request.POST.get('password', '')
        passwordChk = request.POST.get('passwordChk', '')
        phone = request.POST.get('phone', '')
        school = request.POST.get('school','')
        grade = request.POST.get('grade', '')
        sClass = request.POST.get('sClass', '')

        if password != passwordChk:
            return render(request, 'signup.html',{'student':1, 'message':'입력한 비밀번호가 일치하지 않습니다.'})
        else:
            User.objects.create_user(userID=userID, username=username, password = password, phone = phone,school= school, grade= grade, sClass= sClass)
            return redirect(reverse('website:studentSignin'))
    else:
        return render(request, 'signup.html', {'student':1})

def teacherSignup(request):
    if request.method == "POST":
        userID = request.POST['userID']
        username = request.POST.get('username','')
        password = request.POST.get('password', '')
        passwordChk = request.POST.get('passwordChk', '')
        phone = request.POST.get('phone', '')
        school = request.POST.get('school','')
        grade = request.POST.get('grade', '')
        sClass = request.POST.get('sClass', '')

        if password != passwordChk:
            return render(request, 'signup.html',{'student':0, 'message':'입력한 비밀번호가 일치하지 않습니다.'})

        else:
            Teacher.objects.create_teacher(userID=userID, username=username, password = password, phone = phone,school= school, grade= grade, sClass= sClass)
            return redirect(reverse('website:teacherSignin'))
    else:
        return render(request, 'signup.html', {'student':0})

def studentcheckID(request):
    try:
        user= User.objects.get(userID=request.GET['userID'])
    except Exception as e:
        user = None
    result = {
        'result':'success',
        'data':"not exist" if user is None else "exist"
    }
    return JsonResponse(result)

def teachercheckID(request):
    try:
        user= Teacher.objects.get(userID=request.GET['userID'])
    except Exception as e:
        user = None
    result = {
        'result':'success',
        'data':"not exist" if user is None else "exist"
    }
    return JsonResponse(result)

def ajax_schoolInfo_autocomplete(request):
    if 'term' in request.GET:
        search_name = request.GET.get('term','')
        tags = SchoolInfo.objects.filter(name__icontains=search_name)
        print(tags)
        results = []
        for tag in tags:
            tag_json = {}
            tag_json['id'] = tag.id
            tag_json['label'] = tag.name
            tag_json['value'] = tag.name 
            results.append(tag_json)
        data = json.dumps(results)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    return HttpResponse()

@csrf_exempt
def studentSignin(request):
    if request.method == "POST":
        userID = request.POST.get('userID')
        password = request.POST.get('password')

        try:
            user = User.objects.get(userID=userID)
            if user.check_password(password):
                request.session['user'] = user.userID
                return render(request, 'signin.html', {'student':1, 'error' : '성공'})
            else:
                return render(request,'signin.html',{'student':1, 'error':'username or password is incorrect'})
        except:
            return render(request, 'signin.html', {'student':1, 'error': 'username or password is incorrect'})
    else:
        return render(request,'signin.html', {'student':1})

@csrf_exempt
def teacherSignin(request):
    if request.method == "POST":
        userID = request.POST.get('userID', '')
        password = request.POST.get('password', '')
        request.session['user'] = None
        try:
            user = Teacher.objects.get(userID=userID)
            if password == user.password:
                request.session['user'] = user.userID
                return redirect(reverse('website:teacherVideo', args=[1]))
            else:
                return render(request,'signin.html',{'student':0, 'error':'username or password is incorrect'})
        except:
            return render(request, 'signin.html', {'student':0, 'error': 'username or password is incorrect'})
    else:
        return render(request,'signin.html', {'student':0})

@csrf_exempt
def findID(request, student):
    if request.method == "POST":
        username = request.POST.get('username', '')
        phone = request.POST.get('phone', '')

        try:
            if student == 0:
                user = Teacher.objects.get(username=username, phone=phone)
            else:
                user = User.objects.get(username=username, phone=phone)
            return render(request, 'resultID.html', {'userID':user.userID})
        except:
            return render(request, 'findID.html', {'error': 'username or phone is incorrect'})
    else:
        return render(request, 'findID.html')

@csrf_exempt
def findPW(request, student):
    if request.method == "POST":
        username = request.POST.get('username', '')
        userID = request.POST.get('userID', '')
        phone = request.POST.get('phone', '')

        try:
            if student == 0:
                Teacher.objects.get(username=username, userID=userID, phone=phone)
            else:
                User.objects.get(username=username, userID=userID, phone=phone)
            return redirect(reverse('website:resultPW', args=[str(userID)]))
        except:
            return render(request, 'findPW.html', {'error': 'username or phone is incorrect'})
    else:
        return render(request, 'findPW.html')

@csrf_exempt
def resultPW(request, student, userID):
    if request.method == "POST":
        password = request.POST.get('password', '')
        passwordChk = request.POST.get('passwordChk', '')

        try:
            if password == passwordChk:
                if student == 0:
                    user = Teacher.objects.get(userID=userID)
                else:
                    user = User.objects.get(userID=userID)
                user.set_password(password)
                user.save()
                return redirect(reverse('website:studentSignin'))
            else:
                return render(request, 'resultPW.html', {'error': 'password incorrect'})
        except:
            return render(request, 'resultPW.html', {'error': 'password incorrect'})
    else:
        return render(request, 'resultPW.html')

@csrf_exempt
def teacherVideo(request, reportID):
    report = get_object_or_404(Report, id=reportID)

    if request.method == "POST":
        if request.POST.get('feedback1'):
            report.comment1 = request.POST.get('feedback1')
            report.save()
            return redirect(reverse('website:teacherVideo', args=[str(report.id)]))
        elif request.POST.get('feedback2'):
            report.comment2 = request.POST.get('feedback2')
            report.save()
            return redirect(reverse('website:teacherVideo', args=[str(report.id)]))
        elif request.POST.get('feedback3'):
            report.comment3 = request.POST.get('feedback3')
            report.save()
            return redirect(reverse('website:teacherVideo', args=[str(report.id)]))
        if request.POST.get('q_send'):
            return redirect(reverse('website:questionSend', args=[str(report.student.userID)]))

    return render(request, 'studentVideo.html', {'report':report, 'teacher':request.session.get('user')})

@csrf_exempt
def commentDelete1(request, reportID):
    report = get_object_or_404(Report, id=reportID)
    if report.comment1:
        report.comment1 = None
        report.save()
        return redirect(reverse('website:teacherVideo', args=[str(report.id)]))
    return render(request, 'studentVideo.html', {'report': report, 'teacher': request.session.get('user')})

@csrf_exempt
def commentDelete2(request, reportID):
    report = get_object_or_404(Report, id=reportID)
    if report.comment2:
        report.comment2 = None
        report.save()
        return redirect(reverse('website:teacherVideo', args=[str(report.id)]))
    return render(request, 'studentVideo.html', {'report': report, 'teacher': request.session.get('user')})

@csrf_exempt
def commentDelete3(request, reportID):
    report = get_object_or_404(Report, id=reportID)
    if report.comment3:
        report.comment3 = None
        report.save()
        return redirect(reverse('website:teacherVideo', args=[str(report.id)]))
    return render(request, 'studentVideo.html', {'report': report, 'teacher': request.session.get('user')})

@csrf_exempt
def questionSend(request, studentID):

    teacher = get_object_or_404(Teacher, userID=request.session.get('user'))
    studentQ = StudentQuestion.objects.filter(student=studentID, teacher=request.session['user'])

    if request.method == "POST":
        question = request.POST.get('question')
        print(question)
        questionDB = Question.objects.create(question=question, department = -1)
        questionDB.save()
        user = get_object_or_404(User, userID=studentID)
        sQuestionDB = StudentQuestion.objects.create(question=questionDB, student=user, teacher = teacher)
        sQuestionDB.save()
        return render(request, 'questionSend.html', {'questionSet':studentQ})

    return render(request, 'questionSend.html', {'questionSet':studentQ})

@csrf_exempt
def questionSendDelete(request, questionID):
    question = get_object_or_404(Question, id=questionID)
    sQuestion = get_object_or_404(StudentQuestion, question=question)
    user = sQuestion.student
    question.delete()
    return redirect(reverse('website:questionSend', args=[str(user)]))