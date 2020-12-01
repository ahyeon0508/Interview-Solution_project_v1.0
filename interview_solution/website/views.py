from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import User, Teacher, SchoolInfo, Question, StudentQuestion
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

        try:
            user = Teacher.objects.get(userID=userID)
            if check_password(password, user.password):
                request.session['user'] = user.userID
                return render(request, 'signin.html', {'student':0, 'error' : '성공'})
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
def questionList(request):
    if request.session.get('user'):
        # Search
        if request.method == "POST":
            if 'question_search' in request.POST:
                question_search = request.POST.get('question_search','')
                myQuestion = StudentQuestion.objects.filter(student=request.session.get('user'),question=question)
                question = Question.objects.filter(question__contains=question_search)
                question = question.difference(myQuestion)
                if myQuestion.exists() is False and question.exists() is False:
                    return render(request, 'questionList.html', {'error':'해당 질문이 존재하지 않습니다.'})
                return render(request, 'questionList.html', {'question':question, 'myQuestion':myQuestion})
            question = Question.objects.all()
            myQuestion = StudentQuestion.objects.filter(student=request.session.get('user'))
            question = question.difference(myQuestion)
            return render(request, 'questionList.html', {'question': question, 'myQuestion': myQuestion})
        else:
            question = Question.objects.all()
            myQuestion = StudentQuestion.objects.filter(student=request.session.get('user'))
            question = question.difference(myQuestion)
            return render(request, 'questionList.html', {'question': question, 'myQuestion':myQuestion})
    else:
        if request.method=="POST":
            # Search
            if 'question_search' in request.POST:
                question_search = request.POST.get('question_search','')
                question = Question.objects.filter(question__contains=question_search)
                if question.exists() is False:
                    return render(request, 'questionList.html', {'error':'해당 질문이 존재하지 않습니다.'})                    
                return render(request, 'questionList.html', {'question':question})
        question = Question.objects.exclude(department=-1)
        return render(request, 'questionList.html', {'question':question})

@csrf_exempt
def questionStar(request,questionID):
    # Push the star button
    if request.session.get('user'):
        myQuestion = StudentQuestion.objects.filter(student=request.session.get('user'), id=questionID)
        myQuestion.delete()
    return redirect(reverse('website:questionList'))

@csrf_exempt
def questionNonestar(request,questionID):
    # Push the star button
    question = Question.objects.filter(id=questionID)
    myQuestion = StudentQuestion.objects.create(student=request.session.get('user'), teacher=request.session.get('user').teacher,part=0,question=question.question)
    return redirect(reverse('website:questionList'))

def questionListPart(request, q_department):
    if request.session.get('user'):
        if q_department == 1111:
            question = Question.objects.exclude(department=-1).exclude(department=0)
            myQuestion = StudentQuestion.objects.filter(part=0)
            question = question.difference(myQuestion)
            return render(request, 'questionList.html', {'question': question, 'myQuestion':myQuestion})
        question = Question.objects.filter(department=q_department)
        myQuestion = StudentQuestion.objects.filter(part=0)
        question = question.difference(myQuestion)
        return render(request, 'questionList.html', {'question': question, 'myQuestion':myQuestion})
    else:
        if q_department == 1111:
            question = Question.objects.exclude(department=-1).exclude(department=0)
            return render(request, 'questionList.html', {'question': question})
        question = Question.objects.filter(department=q_department)
        return render(request, 'questionList.html', {'question': question})

# myQuestion - 모든 질문, 질문 검색
@csrf_exempt
def myQuestion(request):
    if request.method =="POST":
        if 'question_search' in request.POST:
            question_search = request.POST.get('question_search','')
            try:
                question = Question.objects.filter(question=question_search)
                student_question = StudentQuestion.objects.filter(question=question)
            except:
                return render(request, 'myquestion.html', {'question':question, 'error':'해당 질문이 존재하지 않습니다.'})
            return render(request, 'myquestion.html', {'question':student_question})
    question = StudentQuestion.objects.filter(student=request.session.get('user'))
    return render(request, 'myquestion.html', {'question':question})

# myQuestion - 담은 질문(part: 0)
@csrf_exempt
def myQuestion_contain(request):
    question = StudentQuestion.objects.filter(student=request.session.get('user'),part=0)
    return render(request, 'myquestion.html', {'question':question})

# myQuestion - 작성한 질문 (part: 1)
@csrf_exempt
def myQuestion_write(request):
    question = StudentQuestion.objects.filter(student=request.session.get('user'),part=1)
    return render(request, 'myquestion.html', {'question':question})

# myQuestion - 받은 질문 (part: 2)
@csrf_exempt
def myQuestion_get(request):
    question = StudentQuestion.objects.filter(student=request.session.get('user'),part=2)
    return render(request, 'myquestion.html', {'question':question})

# myQuestion - Question Delete
@csrf_exempt
def deletemyQuestion(request,questionID):
    question = get_object_or_404(StudentQuestion,pk=questionID)
    question.delete()
    return redirect(reverse('website:myQuestion'))
