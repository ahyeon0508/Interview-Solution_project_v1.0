from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import jsonfield

class UserManager(BaseUserManager):
    def create_user(self, userID, password, username=None, phone=None, school=None, grade=None, sClass=None):
        if not userID:
            raise ValueError('ID Required')

        user = self.model(userID=userID, phone=phone, username=username, school=school, grade=grade, sClass=sClass)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userID, password):
        user = self.create_user(userID, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    userID = models.CharField(primary_key=True, unique=True, max_length=10, verbose_name='아이디')  # 아이디
    username = models.CharField(max_length=10, null=True, blank=True, verbose_name='유저이름')
    password = models.CharField(max_length=20, verbose_name='비밀번호')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='연락처')
    school = models.CharField(max_length=10, null=True, blank=True, verbose_name='학교')
    grade = models.CharField(max_length=10, null=True, blank=True, verbose_name='학년')
    sClass = models.CharField(max_length=10, null=True, blank=True, verbose_name='반')
    is_activate = models.BooleanField(default=True)

    USERNAME_FIELD = 'userID'

    objects = UserManager()

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
    question = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='질문')
    department = models.IntegerField(null=True, blank=True, verbose_name='학과') # 0 : 공통질문

    def __str__(self):
        return self.id

class Report(models.Model):  # 수정필요
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name='pk'
    )
    title = models.CharField(max_length=100, default='제목', verbose_name='제목')
    video = models.FileField(blank=True, null=True, upload_to="videos",verbose_name='영상')
    audio = models.FileField(blank=True, null=True, upload_to="videos",verbose_name='음성')
    script = models.CharField(max_length=50000, blank=True, null=True, verbose_name='스크립트')
    adverb = jsonfield.JSONField()
    repetition = jsonfield.JSONField()
    speed = models.FloatField(blank=True, null=True, verbose_name='말하기 속도')
    comment = models.CharField(max_length=10000, blank=True, null=True, verbose_name='댓글')
    pub_date = models.DateField(auto_now_add=True, verbose_name='날짜')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.BooleanField(default=True, verbose_name='공유')
    # 리포트 어떤 거 저장할 것인지 이야기해야함.
    def __str__(self):
        return self.title

class SchoolInfo(models.Model):
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name='pk'
    )
    name = models.CharField(blank=True, null=True, max_length=100)
    def __unicode__(self):
        return self.name