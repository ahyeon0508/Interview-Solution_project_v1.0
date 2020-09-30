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
        extra_kwargs = {"password": {"write_only": True}}

        def create(self, validated_data):
            user = User.objects.create_user(userID=validated_data['userID'], username=validated_data['username'],
                                            password=validated_data['password'], phones=validated_data['phones'],
                                            school=validated_data['school'], grade=validated_data['grade'],
                                            sClass=validated_data['sClass'], year=validated_data['year'])
            # 교사 DB에서 school, grade, sClass 찾기
            return user

class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userID',
                  'username',
                  'phone',
                  'school',
                  'grade',
                  'sClass',
                  'year',
                  'teacher')

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

