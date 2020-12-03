from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from .models import User, Teacher, SchoolInfo, Report, StudentQuestion, Question
import json
import random
from cv2 import cv2
import pyaudio
import wave
from moviepy.editor import *

def intro(request):
    return render(request, 'index.html')

def studentHome(request):
    try:
        user = get_object_or_404(User, userID=request.session['user'])
        return render(request, 'stuhome.html', {'user': user})
    except:
        return render(request, 'stuhome.html', {'user':None})

def teacherHome(request):
    try:
        teacher = get_object_or_404(Teacher, userID=request.session['user'])
        report = Report.objects.filter(teacher=teacher, share=True)
        return render(request, 'teahome.html', {'report':report, 'teacher':teacher})
    except:
        return render(request, 'teahome.html')

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
                return redirect(reverse('website:studentHome'))
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
                return redirect(reverse('website:teacherHome'))
            else:
                return render(request,'signin.html',{'student':0, 'error':'username or password is incorrect'})
        except:
            return render(request, 'signin.html', {'student':0, 'error': 'username or password is incorrect'})
    else:
        return render(request,'signin.html', {'student':0})

@csrf_exempt
def signoff(request):
    if request.session['user']:
        del(request.session['user'])
    return redirect(reverse('website:intro'))

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

def mypage(request):
    if request.method == "POST":
        user = request.session.get('user')
        question = request.POST.get('findQuestion', '')
        answer = request.POST.get('findAnswer', '')
        oldPW = request.POST.get('password', '')
        newPW = request.POST.get('passwordChk', '')
        phone = request.POST.get('phone', '')
        school = request.POST.get('schoolName', '')
        grade = request.POST.get('grade', '')
        if check_password(oldPW, user.password) is False or phone != user.phone or question != user.question or answer != user.answer or school != user.school or grade != user.grade:
            return render(request, 'mypage.html', {'error': '입력한 기존 정보가 잘못되었습니다.'})
        else:
            user.set_password(newPW)
            user.save()
            request.session['user'] = user.userID
            return render(request, 'mypage.html', {'notice': '수정이 완료되었습니다.'})
    else:
        user = User.objects.get(userID=request.session.get('user'))
        return render(request, 'mypage.html', {'user':user})

def secede(request):
    student = get_object_or_404(User, userID=request.session.get('user'))
    student.delete()
    return redirect(reverse('website:intro'))

#질문 리스트 전역변수
interview_list = []
@csrf_exempt
def inter_setting(request):
    # 질문 랜덤으로 정하기
    student = User.objects.get(userID=request.session.get('user'))
    global interview_list
    user_question = StudentQuestion.objects.filter(student=student).values('question')
    n = user_question.count()
    if n < 3:
        for i in range(n):
            question = Question.objects.get(id=user_question[i]['question'])
            interview_list.append(question)
        count = Question.objects.aggregate(count=Count('id'))['count']
        for i in range(n, 3):
            random_index = random.randint(0, count)
            question = Question.objects.all()[random_index]
            interview_list.append(question.question)
    else:
        random_n = random.sample(range(0,n),3)
        for i in random_n:
            question = Question.objects.get(id=user_question[i]['question'])
            interview_list.append(question)
    pub_date = timezone.datetime.now()
    report = Report.objects.create(student=student,teacher=student.teacher,pub_date=pub_date,question1=interview_list[0].question,question2=interview_list[1].question,question3=interview_list[2].question)
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
    userID = request.session.get('user')
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
        RECORD_SECONDS = 45

        video_url = os.path.join(settings.MEDIA_ROOT,reportID+'_'+question_num+'_movie.avi')
        audio_url = os.path.join(settings.MEDIA_ROOT,reportID+'_'+question_num+'_audio.wav')
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
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p_audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        capture.release()
        cv2.destroyAllWindows()
        # video+audio
        video_clip = VideoFileClip(video_url)
        audio_clip = AudioFileClip(audio_url)
        video_clip.audio = audio_clip
        final_url = os.path.join(settings.MEDIA_ROOT, reportID+'_'+question_num+'_final_video.mp4')
        print(final_url)
        video_clip.write_videofile(final_url,codec="mpeg4")

        report = Report.objects.get(id=reportID)
        if question_num=='1':
            report.video1 = final_url
            report.audio1 = audio_url
        elif question_num=='2':
            report.video2 = final_url
            report.audio2 = audio_url
        else:
            report.video3 = final_url
            report.audio3 = audio_url
        report.save()
        
        result = {
            'result':'success'
        }

        return JsonResponse(result)

def interview_q2(request,reportID):
    if request.method == "POST":
        return render(request,'inter_q2.html',{'interview_question':interview_list[1], 'reportID':reportID})
    return render(request,'inter_q2.html',{'interview_question':interview_list[1], 'reportID':reportID})

def interview_q3(request,reportID):
    if request.method == "POST":
        return render(request,'inter_q3.html',{'interview_question':interview_list[2], 'reportID':reportID})
    return render(request,'inter_q3.html',{'interview_question':interview_list[2], 'reportID':reportID})

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
    speech_speed = ""

    # 한글-음절수
    if any(chr.isdigit() for chr in script.replace(" ", "")):
        text_count = len(script.replace(" ", ""))
        numList = re.findall("\d+", script)
        for num in numList:
            text_count -= int(len(num))
            text_count += int(len(readNumber(num)))
        if 4.5 <= text_count / speech_Length <= 5.5:
            speech_speed = "적당한 속도입니다."
        elif  4.5 > text_count / speech_Length:
            speech_speed = "조금 느린 속도입니다."
        else :
            speech_speed = "조금 빠른 속도입니다."

    else:
        text_count = len(script.replace(" ", ""))
        if 4.5 <= text_count / speech_Length <= 5.5:
            speech_speed = "적당한 속도입니다."
        elif 4.5 > text_count / speech_Length:
            speech_speed = "조금 느린 속도입니다."
        else:
            speech_speed = "조금 빠른 속도입니다."

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
    NOUN = []
    for i in range(len(sentence)):
        for j in range(len(sentence[i]['morp'])):
            if sentence[i]['morp'][j]['type'] == 'IC':
                IC.append(sentence[i]['morp'][j]['lemma'])
            elif sentence[i]['morp'][j]['type'] == 'SL':
                SL.append(sentence[i]['morp'][j]['lemma'])
            elif sentence[i]['morp'][j]['type'] == 'NNG' or sentence[i]['morp'][j]['type'] == 'NNP' or \
                    sentence[i]['morp'][j]['type'] == 'NP' or sentence[i]['morp'][j]['type'] == 'NR':
                NOUN.append(sentence[i]['morp'][j]['lemma'])

    IC_counts = Counter(IC)
    adverb = dict(IC_counts.most_common(5))

    NOUN_counts = Counter(NOUN)
    noun_list = []
    for n, c in NOUN_counts.most_common(5):
        if c >= 2:
            noun_list.append((n, c))
    repetition = dict(noun_list)

    return script, text_count, speech_speed, adverb, repetition

def wait(request, reportID):
    report = Report.objects.get(id=reportID)
    if report.audio1:
        report.script1, report.speed1, report.sCorrect1, report.adverb1, report.repetition1 = stt(report.audio1.path)
    if report.audio2:
        report.script2, report.speed2, report.sCorrect1, report.adverb2, report.repetition2 = stt(report.audio2.path)
    if report.audio3:
        report.script3, report.speed3, report.sCorrect1, report.adverb3, report.repetition3 = stt(report.audio3.path)

    report.save()

    if request.method == "POST":
        report.title = request.POST.get('title')
        report.save()
        return render(request, 'wait.html', {'report': report})

    return render(request, 'wait.html', {'report':report})

@csrf_exempt
def waitAjax(request):
    if 'result' in request.POST:
        id = request.POST.get('result')
        one_Report = Report.objects.get(id=id)
        one_Report.share = not(one_Report.share)
        one_Report.save()
        return HttpResponse(one_Report)

def waitVideo1(request, reportID):
    report = Report.objects.get(id=reportID)
    video = report.video1
    return render(request, 'waitVideo.html', {'video':video})

def waitVideo2(request, reportID):
    report = Report.objects.get(id=reportID)
    video = report.video2
    return render(request, 'waitVideo.html', {'video':video})

def waitVideo3(request, reportID):
    report = Report.objects.get(id=reportID)
    video = report.video3
    return render(request, 'waitVideo.html', {'video':video})

@csrf_exempt
def myVideo(request):
    try:
        print(request.session.get('user'))
        report = Report.objects.filter(student=request.session.get('user'))
        return render(request, 'myVideo.html', {'video' : report})
    except:
        return redirect(reverse('website:studentHome'))

@csrf_exempt
def myVideoAjax(request):
    if 'result' in request.POST:
        id = request.POST.get('result')
        one_Report = Report.objects.get(id=id)
        one_Report.share = not(one_Report.share)
        one_Report.save()
        return HttpResponse(one_Report)

@csrf_exempt
def myVideoDetail(request, reportID):
    report = Report.objects.get(id=reportID)
    print(report.student.userID)
    return render(request, 'report.html', {'report':report})

@csrf_exempt
def classVideo(request):
    report = Report.objects.filter(teacher=request.session.get('user').teacher)
    return render(request, 'classVideo.html', {'report' : report})

@csrf_exempt
def classVideoDetail(request, reportID):
    report = Report.objects.get(id=reportID)

    if request.method == "POST":
        report.comment1 = request.POST['comment1']
        report.comment2 = request.POST['comment2']
        report.comment3 = request.POST['comment3']
        report.save()
        return render(request, 'classVideoDetail.html', {'report': report})

    return render(request, 'classVideoDetail.html', {'report':report})

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
@csrf_exempt
def questionList(request):
    if request.session.get('user'):
        # Search
        if request.method == "POST":
            if 'question_search' in request.POST:
                question_search = request.POST.get('question_search','')
                myQuestion = StudentQuestion.objects.filter(student__userID=request.session.get('user'),question__question__contains=question_search)
                question = Question.objects.filter(question__contains=question_search)
                if myQuestion.exists():
                    for i in myQuestion:
                        question = question.exclude(id=i.question.id)
                if myQuestion.exists() is False and question.exists() is False:
                    return render(request, 'questionList.html', {'error':'해당 질문이 존재하지 않습니다.'})

                return render(request, 'questionList.html', {'question':question, 'myQuestion':myQuestion})

            question = Question.objects.all()
            myQuestion = StudentQuestion.objects.filter(student__userID=request.session.get('user'))
            if myQuestion.exists():
                for i in myQuestion:
                    question = question.exclude(id=i.question.id)
            return render(request, 'questionList.html', {'question': question, 'myQuestion': myQuestion})
        else:
            question = Question.objects.all()
            myQuestion = StudentQuestion.objects.filter(student__userID=request.session.get('user'))
            if myQuestion.exists():
                for i in myQuestion:
                    question = question.exclude(id=i.question.id)
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
    myQuestion = StudentQuestion.objects.filter(student__userID=request.session.get('user'), id=questionID)
    myQuestion.delete()
    question = Question.objects.all()
    myQuestion = StudentQuestion.objects.filter(student__userID=request.session.get('user'))
    if myQuestion.exists():
        for i in myQuestion:
            question = question.exclude(id=i.question.id)
    return render(request, 'questionList.html', {'question': question, 'myQuestion': myQuestion})


@csrf_exempt
def questionNonStar(request,questionID):
    # Push the nonstar button
    question = Question.objects.get(id=questionID)
    user = User.objects.get(userID=request.session.get('user'))
    myQuestion = StudentQuestion.objects.create(student=user,part=0,question=question)
    question = Question.objects.all()
    myQuestion = StudentQuestion.objects.filter(student__userID=request.session.get('user'))
    if myQuestion.exists():
        for i in myQuestion:
            question = question.exclude(id=i.question.id)
    return render(request, 'questionList.html', {'question': question, 'myQuestion': myQuestion})

def questionListPart(request, q_department):
    if request.session.get('user'):
        if q_department == 1111:
            question = Question.objects.exclude(department=-1).exclude(department=0)
            myQuestion = StudentQuestion.objects.filter(part=0)
            if myQuestion.exists():
                for i in myQuestion:
                    question = question.exclude(id=i.question.id)
            return render(request, 'questionList.html', {'question': question, 'myQuestion':myQuestion})
        question= Question.objects.filter(department=q_department)
        myQuestion = StudentQuestion.objects.filter(student__userID=request.session.get('user')).filter(question__department=q_department)
        if myQuestion.exists():
            for i in myQuestion:
                question = question.exclude(id=i.question.id)
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

def inter_start(request):
    myQuestion = StudentQuestion.objects.filter(student__userID=request.session.get('user'))
    return render(request, 'inter_start.html', {'myQuestion': myQuestion})

def inter_startPart(request,department):
    question= Question.objects.filter(department=department)
    myQuestion = StudentQuestion.objects.filter(student__userID=request.session.get('user')).filter(question__department=department)
    if myQuestion.exists():
        for i in myQuestion:
            question = question.exclude(id=i.question.id)
    return render(request, 'inter_start.html', {'question': question})

def inter_Star(request, questionID):
    # Push the star button
    myQuestion = StudentQuestion.objects.filter(student__userID=request.session.get('user'), id=questionID)
    myQuestion.delete()
    return redirect(reverse('website:interviewStart'))

def inter_NonStar(request, questionID):
    question = Question.objects.get(id=questionID)
    user = User.objects.get(userID=request.session.get('user'))
    myQuestion = StudentQuestion.objects.create(student=user,part=0,question=question)
    return redirect(reverse('website:interviewStart'))