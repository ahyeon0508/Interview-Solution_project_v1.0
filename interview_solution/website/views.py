from django.shortcuts import render,redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, SchoolInfo
import json
import logging


# Create your views here.

@csrf_exempt
def signup(request):
    if request.method == "POST":
        userID = request.POST['userID']
        username = request.POST.get('username','')
        password = request.POST.get('password', '')
        passwordChk = request.POST.get('passwordChk', '')
        phone = request.POST.get('phone', '')
        school = request.POST.get('school','')
        grade = request.POST.get('grade', '')
        sClass = request.POST.get('sClass', '')
        year = request.POST.get('year', '')

        if password != passwordChk:
            return render(request, 'signup.html',{'error':'wrong'})

        else:
            User.objects.create_user(userID=userID, username=username, password = password, phone = phone,school= school, grade= grade, sClass= sClass, year= year)
            return redirect('/')
    else:
        return render(request, 'signup.html',{'error':'wrong'})
    
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