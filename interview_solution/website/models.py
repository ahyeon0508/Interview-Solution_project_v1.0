from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.
class TeacherManager(BaseUserManager):
    def create_teacher(self, userID, username, password, phone, school, grade, sClass):
        teacher = self.model(userID=userID, username=username, password=password, phone=phone, school=school, grade=grade, sClass=sClass)
        teacher.save(using=self._db)
        return teacher

class Teacher(models.Model):
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name='pk'
    )
    userID = models.CharField(unique=True, max_length=10, verbose_name = '아이디') #아이디
    username = models.CharField(max_length=10, null=True, blank=True, verbose_name='유저이름')
    password = models.CharField(max_length=20, verbose_name = '비밀번호')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name = '연락처')
    school = models.CharField(max_length=15, null=True, blank=True, verbose_name='학교')
    grade = models.IntegerField(null=True, blank=True, verbose_name='학년')
    sClass = models.IntegerField(null=True, blank=True, verbose_name='반')
    is_activate = models.BooleanField(default=True)

    USERNAME_FIELD = 'userID'

    objects=TeacherManager()

    def __str__(self):
        return self.userID

class UserManager(BaseUserManager):
    def create_user(self, userID, password, username=None, phone=None, school=None, grade=None, sClass=None, year=2020):
        if not userID:
            raise ValueError('ID Required')

        user = self.model(userID=userID, phone=phone, username=username, school=school, grade=grade, sClass=sClass, year=year)
        try:
            teacher = Teacher.objects.get(school=school, grade=grade, sClass=sClass)
            user.teacher = teacher
        except ObjectDoesNotExist:
            pass
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userID, password):
        user = self.create_user(userID, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name='pk'
    )
    userID = models.CharField(unique=True, max_length=10, verbose_name = '아이디') #아이디
    username = models.CharField(max_length=10, null=True, blank=True, verbose_name='유저이름')
    password = models.CharField(max_length=20, verbose_name = '비밀번호')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name = '연락처')
    school = models.CharField(max_length=10, null=True, blank=True, verbose_name='학교')
    grade = models.CharField(max_length=10, null=True, blank=True, verbose_name='학년')
    sClass = models.CharField(max_length=10, null=True, blank=True, verbose_name='반')
    year = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name='연도') # 년도만 빼내기
    teacher = models.ForeignKey(Teacher, null=True, on_delete= models.SET_NULL, related_name='teacher')
    is_activate = models.BooleanField(default=True)

    USERNAME_FIELD = 'userID'

    objects=UserManager()

    def __str__(self):
        return self.userID

    def is_staff(self):
        "Is the user a memeber of staff?"
        return self.is_superuser

class Question(models.Model):
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name='pk'
    )
    question = models.CharField(max_length=100, null=True, blank=True, verbose_name='질문')

    def __str__(self):
        return self.id

class StudentQuestion(models.Model):
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name='pk'
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_question')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_question')

class Report(models.Model): # 수정필요
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name='pk'
    )
    video = models.URLField(blank=True, null=True, verbose_name='영상 url')
    # 리포트 어떤 거 저장할 것인지 이야기해야함.

    def __str__(self):
        return self.id
    
class Comment(models.Model):
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name='pk'
    )
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name='댓글')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='comment')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comment')

class SchoolInfo(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __unicode__(self):
        return self.name