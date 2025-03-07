from django.db import models

from django.db.models import Model

class StudentModel(Model):

    rno=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    year=models.CharField(max_length=50)
    section=models.CharField(max_length=50)
    branch=models.CharField(max_length=50)
    otp = models.CharField(max_length=50, default="")
    isverified = models.CharField(max_length=50, default="")
    status = models.CharField(max_length=50)

class AttendanceModel(Model):
    studentid=models.CharField(max_length=50)
    date=models.CharField(max_length=50)
    intime=models.CharField(max_length=50)
    outtime=models.CharField(max_length=50)
    branch=models.CharField(max_length=50)
    isattended = models.CharField(max_length=50)

class FacultyModel(Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    branch=models.CharField(max_length=50)