from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User


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
            return render(request,'signup.html')
    else:
        return render(request, 'signup.html',{'error':'wrong'})
    