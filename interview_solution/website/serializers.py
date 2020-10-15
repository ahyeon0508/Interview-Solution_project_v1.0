<<<<<<< HEAD
from rest_framework import serializers
from .models import User, Teacher, Question, StudentQuestion, Report, Comment
from django.contrib.auth import authenticate

class SignupUserSerializer(serializers.ModelSerializer):
    passwordChk = serializers.CharField(max_length=20,)

    class Meta:
        model = User
        fields = ('userID',
                  'username',
                  'phone',
                  'school',
                  'grade',
                  'sClass',
                  'year')

        extra_kwargs = {"password": {"write_only": True},"passwordChk": {"write_only": True}}

        def create(self, validated_data):
            user = User.objects.create_user(userID=validated_data['userID'], username=validated_data['username'],
                                            password=validated_data['password'], phone=validated_data['phone'],
                                            school=validated_data['school'], grade=validated_data['grade'],
                                            sClass=validated_data['sClass'], year=validated_data['year'])
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
=======
from rest_framework import serializers
from .models import User, Teacher, Question, StudentQuestion, Report, Comment
from django.contrib.auth import authenticate

class SignupUserSerializer(serializers.ModelSerializer):
    passwordChk = serializers.CharField(max_length=20,)

    class Meta:
        model = User
        fields = ('userID',
                  'username',
                  'phone',
                  'school',
                  'grade',
                  'sClass',
                  'year')

        extra_kwargs = {"password": {"write_only": True},"passwordChk": {"write_only": True}}

        def create(self, validated_data):
            user = User.objects.create_user(userID=validated_data['userID'], username=validated_data['username'],
                                            password=validated_data['password'], phone=validated_data['phone'],
                                            school=validated_data['school'], grade=validated_data['grade'],
                                            sClass=validated_data['sClass'], year=validated_data['year'])
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

class CheckToChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    userID = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    passwordChk = serializers.CharField(required=True)

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ()
>>>>>>> cb5195591566723db54cfc312433fc8d04b1d30e
