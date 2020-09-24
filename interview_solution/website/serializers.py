from rest_framework import serializers
from .models import User, Teacher, Question, StudentQuestion, Report, Comment
from django.contrib.auth import authenticate

class SignupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userID',
                  'username',
                  'password',
                  'phone',
                  'school',
                  'grade',
                  'sClass',
                  'year')

class SigninUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userID', 'password')

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ()

