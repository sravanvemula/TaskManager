from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete='')
    def __str__(self):
        return self.user.username

class Status(models.Model):
    statusId = models.IntegerField(primary_key=True)
    statusValue = models.CharField(max_length=100)

    def __str__(self):
        return self.statusValue

class Tasks(models.Model):
    taskId = models.CharField(max_length=10)
    taskName = models.CharField(max_length=70)
    taskDescription = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True,blank=True)
    createdBy = models.CharField(max_length=30)
    assignedTo = models.CharField(max_length=30)
    lastModifiedDate = models.DateTimeField(auto_now_add=True,blank=True)
    lastModifiedBy = models.CharField(max_length=30)
    remarks = models.TextField()
    status = models.ForeignKey(Status, on_delete='', default=1)

    def __str__(self):
        return self.taskId


class Drafts(models.Model):
    taskId = models.CharField(max_length=10)
    taskName = models.CharField(max_length=70)
    taskDescription = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True,blank=True)
    createdBy = models.CharField(max_length=30)
    assignedTo = models.CharField(max_length=30)
    lastModifiedDate = models.DateTimeField(auto_now_add=True,blank=True)
    lastModifiedBy = models.CharField(max_length=30)
    remarks = models.TextField()
    status = models.ForeignKey(Status, on_delete='', default=4)
    def __str__(self):
        return self.taskId
