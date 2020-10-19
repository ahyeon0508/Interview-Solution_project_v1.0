from django.shortcuts import render,redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

from .models import User, Teacher, SchoolInfo, StudentQuestion
import json
import logging
import random
import datetime
from cv2 import cv2
import pyaudio
import wave
from moviepy.editor import *
import time
from django.core.files.storage import default_storage

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
            return render(request, 'signup.html',{'message':'입력한 비밀번호가 일치하지 않습니다.'})
        else:
            User.objects.create_user(userID=userID, username=username, password = password, phone = phone,school= school, grade= grade, sClass= sClass)
            return redirect(reverse('website:studentSignin'))
    else:
        return render(request, 'signup.html',{'message':'회원가입 실패'})

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
            return render(request, 'signup.html',{'message':'입력한 비밀번호가 일치하지 않습니다.'})

        else:
            Teacher.objects.create_teacher(userID=userID, username=username, password = password, phone = phone,school= school, grade= grade, sClass= sClass)
            return redirect(reverse('website:teacherSignin'))
    else:
        return render(request, 'signup.html',{'message':'회원가입 실패'})

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
                return render(request, 'signin.html', {'error' : '성공'})
            else:
                return render(request,'signin.html',{'error':'username or password is incorrect'})
        except:
            return render(request, 'signin.html', {'error': 'username or password is incorrect'})
    else:
        return render(request,'signin.html')

@csrf_exempt
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

@csrf_exempt
def findID(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        phone = request.POST.get('phone', '')

        try:
            user = User.objects.get(username=username, phone=phone)
            return render(request, 'resultID.html', {'userID':user.userID})
        except:
            return render(request, 'findID.html', {'error': 'username or phone is incorrect'})
    else:
        return render(request, 'findID.html')

@csrf_exempt
def findPW(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        userID = request.POST.get('userID', '')
        phone = request.POST.get('phone', '')

        try:
            print("A")
            User.objects.get(username=username, userID=userID, phone=phone)
            print("B")
            return redirect(reverse('website:resultPW', args=[str(userID)]))
        except:
            return render(request, 'findPW.html', {'error': 'username or phone is incorrect'})
    else:
        return render(request, 'findPW.html')

@csrf_exempt
def resultPW(request, userID):
    if request.method == "POST":
        password = request.POST.get('password', '')
        passwordChk = request.POST.get('passwordChk', '')

        try:
            if password == passwordChk:
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

#질문 리스트 전역변수
interview_list = ['a','b','c']
def inter_setting(request):
    # 질문 랜덤으로 정하기
    user_question = StudentQuestion.objects.filter(student=request.user).values('question')
    n = user_question.count()
    if n < 3:
        interview_list = user_question
    else:
        random_n = random.sample(range(0,n),3)
        for i in range(3):
            interview_list.append(user_question[random_n[i]])
    return render(request,'inter_setting.html')

frames =[]
def interview_q1(request):
    if request.method == "POST":
        print('a')
        
        return render(request,'inter_q1.html',{'interview_question':interview_list[0]})
    else:
        return render(request,'inter_q1.html',{'interview_question':interview_list[0]}) 
@csrf_exempt
def recordVideo(request):
    userID = request.POST['userID']
    question_num = request.POST['question']
    if request.POST.get('start',True):
        del frames[:]
        # OPENCV
        capture = cv2.VideoCapture(0)
         # 코덱 정보(인코딩 방식)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #PyAudio
        CHUNK = 1024
        RATE = 16000 # 음성 데이터의 Sampling Rate: 16000Hz
        
        start = time.time()
        i=0
        while True:
            ret, frame = capture.read()
            cv2.imshow('Camera Window', frame)
            key = cv2.waitKey(33)
            if time.time()-start > 90:
                break
            if i==0:
                video_url = os.path.join(settings.MEDIA_ROOT,userID+'_'+question_num+'_movie.avi')
                audio_url = os.path.join(settings.MEDIA_ROOT,userID+'_'+question_num+'_audio.wav')
                video = cv2.VideoWriter(video_url, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                p_audio = pyaudio.PyAudio()
                audio_stream = p_audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
                i=1
            video.write(frame)
            data = audio_stream.read(CHUNK)
            frames.append(data)
            print("녹화 중..")
            if key==27:
                print("kk")
        video.release()
        audio_stream.stop_stream()
        audio_stream.close()
        p_audio.terminate()
        
        wf = wave.open(audio_url, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p_audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        capture.release()
        cv2.destroyAllWindows()   
        video_clip = VideoFileClip(video_url)
        audio_clip = AudioFileClip(audio_url)
        video_clip.audio = audio_clip
        final_url = os.path.join(settings.MEDIA_ROOT,userID+'_'+question_num+'_final_video.mp4')
        video_clip.write_videofile(final_url,codec="mpeg4")
        result = {
            'result':'success'
        }
        return JsonResponse(result)
    if request.POST.get('finish',True):
        video.release()
        audio_stream.stop_stream()
        audio_stream.close()
        p_audio.terminate()
        wf = wave.open(audio_url, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p_audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        capture.release()
        cv2.destroyAllWindows()   
        video_clip = VideoFileClip(video_url)
        audio_clip = AudioFileClip(audio_url)
        video_clip.audio = audio_clip
        final_url = os.path.join(settings.MEDIA_ROOT,userID+'_'+question_num+'_final_video.mp4')
        video_clip.write_videofile(final_url,codec="mpeg4")
    
def interview_q2(request):
    if request.method == "POST":
        return render(request,'inter_q2.html',{'interview_question':interview_list[1]})
    return render(request,'inter_q2.html')

def interview_q3(request):
    if request.method == "POST":
        
        return render(request,'inter_setting.html',{'interview_question':interview_list[2]})
    return render(request,'inter_setting.html')