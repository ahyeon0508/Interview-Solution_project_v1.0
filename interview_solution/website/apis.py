from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from requests import Response
from rest_framework import viewsets, permissions, generics, status
from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.utils import json
from rest_framework.views import APIView

from .models import User
from .serializers import (
    SignupUserSerializer,
    SigninUserSerializer,
    UserViewSerializer,
    ChangePasswordSerializer,
    CheckToChangePasswordSerializer,
)

class SigninUserAPI(GenericAPIView):
    serializer_class = SigninUserSerializer
    renderer_classes = (TemplateHTMLRenderer,)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = User.objects.get(userID=data['userID'])

        if check_password(data['password'], user.password):
            return Response({"message": "로그인에 성공하셨습니다."}, template_name='signin.html')
        else:
            return Response({'message' : '실패'}, template_name='signin.html')

class GetIDAPI(APIView):
    serializer_class = UserViewSerializer
    model = User

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if User.objects.filter(username=serializer.data.get("username")) is not None:
            return Response({'userID' : User.objects.get(username=serializer.data.get("username"))}, template_name='resultID.html')
        return Response({'message' : '실패'}, template_name='findID.html')

class CheckToChangePasswordAPI(APIView):
    serializer_class = CheckToChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if User.objects.filter(username=serializer.data.get("username"), userID=serializer.data.get("userID"), phone=serializer.data.get("phone")) is not None:
                return redirect(reverse('website:changePW'))
            else:
                return Response(serializer.errors, template_name='findPW.html')

        return Response(serializer.errors, template_name='findPW.html')

class ChangePasswordAPI(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if serializer.data.get("password") == serializer.data.get("passwordChk") :
                self.object.set_password(serializer.data.get("password"))
                self.object.save()
                return Response("Success.", template_name='signin.html')
            else:
                return Response(serializer.errors, template_name='resultPW.html')

        return Response(serializer.errors, template_name='resultPW.html')