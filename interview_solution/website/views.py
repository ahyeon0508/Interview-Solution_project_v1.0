from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from django.db.models.aggregates import Count
from random import randint

from .models import User, SchoolInfo, Report, Question
import json
import random
from cv2 import cv2
import pyaudio
import wave
from moviepy.editor import *

def readNumber(num):
    units = [''] + list('십백천')
    nums = ['', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
    result = []
    i = 0
    n = int(num)
    while n > 0:
        n, r = divmod(n, 10)
        if r > 0:
            result.append(nums[r-1] + units[i])
        i += 1
    return ''.join(result[::-1])

def isEng(value):
    count = 0
    for c in value:
        if ord('a') <= ord(c.lower()) <= ord('z'):
            count += 1
    if len(value) == count:
        return True

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
                return redirect('website:interviewSetting')
            else:
                return render(request,'signin.html',{'student':1, 'error':'username or password is incorrect'})
        except:
            return render(request, 'signin.html', {'student':1, 'error': 'username or password is incorrect'})
    else:
        return render(request,'signin.html', {'student':1})

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
            User.objects.get(username=username, userID=userID, phone=phone)
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
interview_list = []
@csrf_exempt
def inter_setting(request):
    # 질문 랜덤으로 정하기
    student = User.objects.get(userID=request.session.get('user'))
    global interview_list
    count = Question.objects.aggregate(count=Count('id'))['count']
    random_index = randint(0, count - 1)
    user_question = Question.objects.all()[random_index]
    interview_list.append(user_question.question)
    pub_date = timezone.datetime.now()
    report = Report.objects.create(student=student, pub_date=pub_date)
    report.save()
    reportID = report.id
    return render(request, 'inter_setting.html',{'reportID':reportID})

def interview_q1(request,reportID):
    if request.method == "POST":        
        return render(request,'inter_q1.html',{'interview_question':interview_list[0], 'reportID':reportID})
    else:
        return render(request,'inter_q1.html',{'interview_question':interview_list[0], 'reportID':reportID})

stop_button = 0
@csrf_exempt
def stop_button_q1(request):
    if request.POST.get('finish',True):
        global stop_button
        stop_button = 1
        print("press the button")
        result = {
            'result':'success'
        }
        return JsonResponse(result)

frames =[]
@csrf_exempt
def recordVideo(request):
    global stop_button
    userID = request.POST['userID']
    question_num = request.POST['question']
    reportID = request.POST['reportID']
    if request.POST.get('start',True):
        del frames[:]
        # OPENCV
        capture = cv2.VideoCapture(0)
        # 코덱 정보(인코딩 방식)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #PyAudio
        CHUNK = 1024
        RATE = 16000 # 음성 데이터의 Sampling Rate: 16000Hz
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RECORD_SECONDS = 20

        video_url = os.path.join(settings.MEDIA_ROOT,userID+'_'+question_num+'_movie.avi')
        audio_url = os.path.join(settings.MEDIA_ROOT,userID+'_'+question_num+'_audio.wav')
        ret, frame = capture.read()
        video = cv2.VideoWriter(video_url, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
        p_audio = pyaudio.PyAudio()
        audio_stream = p_audio.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

        print("* recording")

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): # wav는 녹음시 한계가 필요하기 때문에 수정함
            if stop_button==1:
                ret, frame = capture.read()
                video.write(frame)
                data = audio_stream.read(CHUNK)
                frames.append(data)
                break
            ret, frame = capture.read()
            video.write(frame)
            data = audio_stream.read(CHUNK)
            frames.append(data)
            print("%d : 녹화 중..", stop_button)

        print("* done recording")

        stop_button = 0

        video.release()
        audio_stream.stop_stream()
        audio_stream.close()
        p_audio.terminate()

        wf = wave.open(audio_url, 'wb')
        print("A")
        wf.setnchannels(CHANNELS)
        print("A")
        wf.setsampwidth(p_audio.get_sample_size(FORMAT))
        print("A")
        wf.setframerate(RATE)
        print("A")
        wf.writeframes(b''.join(frames))
        print("A")
        wf.close()
        print("A")

        capture.release()
        cv2.destroyAllWindows()
        # video+audio
        video_clip = VideoFileClip(video_url)
        audio_clip = AudioFileClip(audio_url)
        video_clip.audio = audio_clip
        final_url = os.path.join(settings.MEDIA_ROOT, userID+'_'+question_num+'_final_video.mp4')
        video_clip.write_videofile(final_url,codec="mpeg4")

        print("A")
        report = Report.objects.get(id=reportID)
        report.video = final_url
        report.audio = audio_url
        report.save()

        print(report.video)
        
        result = {
            'result':'success'
        }

        return JsonResponse(result)

def stt(audiofile):
    import base64
    import re
    import wave
    import urllib3
    import json
    from collections import Counter
    from ast import literal_eval
    from konlpy.tag import Okt

    def readNumber(num):
        units = [''] + list('십백천')
        nums = ['', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
        result = []
        i = 0
        n = int(num)
        while n > 0:
            n, r = divmod(n, 10)
            if r > 0:
                result.append(nums[r - 1] + units[i])
            i += 1
        return ''.join(result[::-1])

    def get_time(audio_path):
        audio = wave.open(audio_path)
        frames = audio.getnframes()
        rate = audio.getframerate()
        time = frames / float(rate)
        return time

    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    accessKey = "1a2937a3-caef-42ee-9b2d-4eadaf9c78c9"
    languageCode = "korean"

    audiopath = audiofile
    file = open(audiopath, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "language_code": languageCode,
            "audio": audioContents
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )

    data = str(response.data, "utf-8")
    dict_data = literal_eval(data)
    result = dict_data['return_object']['recognized']

    # 기록
    script = result

    # 음성파일 시간
    speech_Length = get_time(audiopath)

    # 말하기 속도
    text_count = 0
    numList = []
    speech_speed = 0.0

    # 한글-음절수
    if any(chr.isdigit() for chr in script.replace(" ", "")):
        text_count = len(script.replace(" ", ""))
        numList = re.findall("\d+", script)
        for num in numList:
            text_count -= int(len(num))
            text_count += int(len(readNumber(num)))
        speech_speed = text_count / speech_Length

    else:
        text_count = len(script.replace(" ", ""))
        speech_speed = text_count / speech_Length

    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken"

    accessKey = "1a2937a3-caef-42ee-9b2d-4eadaf9c78c9"
    analysisCode = "morp"

    text = script

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": text,
            "analysis_code": analysisCode
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )

    data = str(response.data, "utf-8")
    dict_data = literal_eval(data)
    sentence = dict_data['return_object']['sentence']

    # 감탄사 추출
    IC = []
    SL = []
    for i in range(len(sentence)):
        for j in range(len(sentence[i]['morp'])):
            if sentence[i]['morp'][j]['type'] == 'IC':
                IC.append(sentence[i]['morp'][j]['lemma'])
            elif sentence[i]['morp'][j]['type'] == 'SL':
                SL.append(sentence[i]['morp'][j]['lemma'])

    IC_counts = Counter(IC)
    adverb = dict(IC_counts.most_common(5))
    print(adverb)

    # 명사 추출
    okt = Okt()
    okt_noun = okt.nouns(text)
    noun = [x for x in okt_noun if x not in IC]
    noun += SL
    print(noun)
    noun_counts = Counter(noun)
    noun_list = []
    for n, c in noun_counts.most_common(5):
        if c >= 2:
            noun_list.append((n, c))
    repetition = dict(noun_list)
    print(repetition)

    return script, speech_speed, adverb, repetition

def wait(request, reportID):
    report = Report.objects.get(id=reportID)
    report.script, report.speed, report.adverb, report.repetition = stt('./videos/videos/jin_1_audio.wav')

    report.save()

    return render(request, 'wait.html', {'IQ1':'안녕하세요', 'report':report})

def waitVideo1(request, reportID):
    report = Report.objects.get(id=reportID)
    video = report.video
    return render(request, 'waitVideo.html', {'video':video})

@csrf_exempt
def myVideo(request):
    if request.is_ajax():
        print("A")
        id = request.POST.get('result')
        one_Report = Report.objects.get(id=id)
        one_Report.share = not(one_Report.share)
        print(one_Report.share)
        one_Report.save()
        report = Report.objects.filter(student=request.session.get('user'))
        return render(request, 'myVideo.html', {'report' : report})

    report = Report.objects.filter(student=request.session.get('user'))
    return render(request, 'myVideo.html', {'report' : report, 'user':request.session.get('user')})

@csrf_exempt
def myVideoDetail(request, reportID):
    report = Report.objects.get(id=reportID)
    report.script, report.speed, report.adverb, report.repetition = stt('./videos/videos/jin_1_audio.wav')

    report.save()

    report = Report.objects.get(id=reportID)
    return render(request, 'report.html', {'report':report})
