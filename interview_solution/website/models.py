from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import jsonfield

# Create your models here.
class TeacherManager(BaseUserManager):
    def create_teacher(self, userID, username, password, phone, school, grade, sClass):
        teacher = self.model(userID=userID, username=username, password=password, phone=phone, school=school,
                             grade=grade, sClass=sClass)
        teacher.save(using=self._db)
        return teacher

class Teacher(models.Model):
    userID = models.CharField(primary_key=True, unique=True, max_length=10, verbose_name='아이디')  # 아이디
    username = models.CharField(max_length=10, null=True, blank=True, verbose_name='유저이름')
    password = models.CharField(max_length=20, verbose_name='비밀번호')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='연락처')
    school = models.CharField(max_length=15, null=True, blank=True, verbose_name='학교')
    grade = models.IntegerField(null=True, blank=True, verbose_name='학년')
    sClass = models.IntegerField(null=True, blank=True, verbose_name='반')
    is_activate = models.BooleanField(default=True)

    USERNAME_FIELD = 'userID'

    objects = TeacherManager()

    def __str__(self):
        return self.userID

class UserManager(BaseUserManager):
    def create_user(self, userID, password, username=None, phone=None, school=None, grade=None, sClass=None):
        if not userID:
            raise ValueError('ID Required')

        user = self.model(userID=userID, phone=phone, username=username, school=school, grade=grade, sClass=sClass)
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
    userID = models.CharField(primary_key=True, unique=True, max_length=10, verbose_name='아이디')  # 아이디
    username = models.CharField(max_length=10, null=True, blank=True, verbose_name='유저이름')
    password = models.CharField(max_length=100, verbose_name='비밀번호')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='연락처')
    school = models.CharField(max_length=20, null=True, blank=True, verbose_name='학교')
    grade = models.IntegerField(null=True, blank=True, verbose_name='학년')
    sClass = models.IntegerField(null=True, blank=True, verbose_name='반')
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.CASCADE)
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
    question = models.CharField(max_length=100, null=True, blank=True, verbose_name='질문')
    department = models.IntegerField(null=True, blank=True, verbose_name='학과') # 0 : 공통질문, -1 : 개인질문

    def __int__(self):
        return self.id

class StudentQuestion(models.Model):
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name='pk'
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.CASCADE)

    def __int__(self):
        return self.id

class Report(models.Model):  # 수정필요
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name='pk'
    )
    title = models.CharField(max_length=100, default='제목', verbose_name='제목')
    question1 = models.CharField(max_length=50000, blank=True, null=True, verbose_name='질문1')
    question2 = models.CharField(max_length=50000, blank=True, null=True, verbose_name='질문2')
    question3 = models.CharField(max_length=50000, blank=True, null=True, verbose_name='질문3')
    video1 = models.FileField(blank=True, null=True, upload_to="videos",verbose_name='영상1')
    video2 = models.FileField(blank=True, null=True, upload_to="videos",verbose_name='영상2')
    video3 = models.FileField(blank=True, null=True, upload_to="videos",verbose_name='영상3')
    audio1 = models.FileField(blank=True, null=True, upload_to="videos",verbose_name='음성1')
    audio2 = models.FileField(blank=True, null=True, upload_to="videos",verbose_name='음성2')
    audio3 = models.FileField(blank=True, null=True, upload_to="videos",verbose_name='음성3')
    script1 = models.CharField(max_length=50000, blank=True, null=True, verbose_name='스크립트1')
    script2 = models.CharField(max_length=50000, blank=True, null=True, verbose_name='스크립트2')
    script3 = models.CharField(max_length=50000, blank=True, null=True, verbose_name='스크립트3')
    adverb1 = jsonfield.JSONField()
    adverb2 = jsonfield.JSONField()
    adverb3 = jsonfield.JSONField()
    repetition1 = jsonfield.JSONField()
    repetition2 = jsonfield.JSONField()
    repetition3 = jsonfield.JSONField()
    speed1 = models.FloatField(blank=True, null=True, verbose_name='말하기 속도1')
    speed2 = models.FloatField(blank=True, null=True, verbose_name='말하기 속도2')
    speed3 = models.FloatField(blank=True, null=True, verbose_name='말하기 속도3')
    sCorrect1 = models.CharField(max_length=10000, blank=True, null=True,  verbose_name='말하기 속도1')
    sCorrect2 = models.CharField(max_length=10000, blank=True, null=True,  verbose_name='말하기 속도2')
    sCorrect3 = models.CharField(max_length=10000, blank=True, null=True,  verbose_name='말하기 속도3')
    comment1 = models.CharField(max_length=10000, blank=True, null=True, verbose_name='댓글1')
    comment2 = models.CharField(max_length=10000, blank=True, null=True, verbose_name='댓글2')
    comment3 = models.CharField(max_length=10000, blank=True, null=True, verbose_name='댓글3')
    pub_date = models.DateField(auto_now_add=True, verbose_name='날짜')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,null=True, blank=True, on_delete=models.CASCADE)
    share = models.BooleanField(default=False, verbose_name='공유')

    def __int__(self):
        return self.id

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