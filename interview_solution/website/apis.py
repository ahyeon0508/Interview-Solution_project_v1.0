from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.utils import json
from rest_framework.views import APIView

from .models import User
from .serializers import (
    SignupUserSerializer,
    SigninUserSerializer,
)

class SigninUserAPI(generics.GenericAPIView):
    serializer_class = SigninUserSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = User.objects.get(userID=data['userID'])

        if check_password(data['password'], user.password):
            return JsonResponse({"message": "로그인에 성공하셨습니다."}, status=200)
        else:
            return JsonResponse({'message' : '실패'}, status=400)