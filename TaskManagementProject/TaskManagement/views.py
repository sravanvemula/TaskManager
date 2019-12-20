from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from TaskManagement import forms
from django.urls import reverse
import mimetypes
from django.utils.encoding import smart_str
import os
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from TaskManagement.models import Tasks, Status, Drafts
from django.views.generic.edit import FormView, CreateView
from random import randint
import datetime
from TaskManagementProject import settings
from wsgiref.util import FileWrapper
import pandas as pd
import json
from django.core.files.storage import default_storage
# Create your views here
def index(request):
    my_dict = {'insert_me':"Welcome to the Home page"}
    if request.method =='POST':
        return homePage(request)
    return render(request,'TaskManagement/index.html',context=my_dict)

@login_required
def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/TaskManagement/')

def register(request):
    registerd = False

    if request.method == 'POST':
        userform = forms.UserForm(request.POST)

        if userform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            registerd = True
        else:
            print(userform.errors)
    else:
        userform = forms.UserForm()
    return render(request, 'TaskManagement/registration.html',{'UserForm':userform,'registered':registerd})



def userLogin(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                tasks = Tasks.objects.order_by('taskId')
                data = {
                'user': user,
                'tasks':tasks
                }
                request.session['tasks'] = data['tasks']
                request.session['user'] = data['user']
                return render(request,'TaskManagement/homePage.html',data)
            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login and failed")
            print("username: {} and passowrd: {}".format(username,password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'TaskManagement/login.html',{})

@login_required
def homePage(request):
    tasks = Tasks.objects.order_by('taskId')
    user = request.session['user']
    data = {
    'user': user,
    'tasks':tasks
    }
    return render(request,'TaskManagement/homePage.html',data)

@login_required
def assignedToMe(request):
    user = request.session['user']
    tasks = Tasks.objects.filter(assignedTo=user)
    data = {
    'user':user,
    'tasks':tasks
    }
    return render(request,'TaskManagement/assignedtome.html',data)

@login_required
def createdByMe(request):
    user = request.session['user']
    tasks = Tasks.objects.filter(createdBy=user)
    data = {
    'user':user,
    'tasks':tasks
    }
    return render(request,'TaskManagement/createdbyme.html',data)


@login_required
def createNewTask(request):
    user = request.session['user']
    listofusers = User.objects.all()
    print(list(request.POST))
    if request.method == 'POST' and 'createtask' in list(request.POST):
        print("i am in create")
        form = forms.CreateNewTaskForm(request.POST)
        listForm = forms.selectUserForm(request.POST)
        if form.is_valid() and listForm.is_valid():
            task = form.save(commit=False)
            task.createdBy = user
            task.lastModifiedBy = user
            task.taskId = 'TASK'+str(randint(1111,9999))
            task.assignedTo = listForm.cleaned_data['Assignto']
            # status=Status.objects.filter(statusId__exact=1)
            # task.status=status['statusId']
            task.save()
            ##generate auto task id
            return HttpResponseRedirect('/TaskManagement/createdbyme/')
    elif request.method == 'POST' and 'savetask' in list(request.POST):
        print('I am in save')
        form = forms.CreateNewTaskForm(request.POST)
        listForm = forms.selectUserForm(request.POST)
        if form.is_valid() and listForm.is_valid():
            task = form.save(commit=False)
            draft = Drafts()
            draft.taskId = task.taskId
            draft.taskName = task.taskName
            draft.taskDescription = task.taskDescription
            draft.assignedTo = task.assignedTo
            draft.remarks = task.remarks
            draft.createdBy = user
            draft.lastModifiedBy = user
            draft.taskId = 'TASK'+str(randint(1111,9999))
            draft.assignedTo = listForm.cleaned_data['Assignto']
            draft.save()
            return showdrafts(request)

        else:
            print(form.errors)
    else:
        form = forms.CreateNewTaskForm()
        listForm = forms.selectUserForm()
    data={
    'user':user,
    'form':form,
    'listForm':listForm,
    'users':listofusers,
    }
    return render(request,'TaskManagement/createnewtask.html',data)

@login_required
def updateTask(request):
    user = request.session['user']
    taskDetails = Tasks.objects.filter(assignedTo=user)
    form=forms.selectTaskForm()
    print(user, taskDetails)
    dictionary = {
        'user':user,
        'taskDetails':taskDetails,
        'form': form
    }
    if request.method == 'POST':
        form = forms.selectTaskForm(request.POST)
        print(request.POST.get('TaskId'))
        Tasks.objects.filter(taskId=request.POST.get('TaskId')).update(status=request.POST.get('status'),remarks=request.POST.get('remarks'))
        #return render(request,'TaskManagement/assignedtome.html',{'user':user})
        return HttpResponseRedirect('/TaskManagement/assignedtome/')
    else:
        form=forms.selectTaskForm(user)
    return render(request,'TaskManagement/updateTask.html',context=dictionary)

@login_required
def showdrafts(request):
    user = request.session['user']
    tasks = Drafts.objects.filter(createdBy=user)
    data = {
    'user':user,
    'tasks':tasks
    }
    return render(request,'TaskManagement/drafts.html',data)

@login_required()
def editAndSubmit(request):
    user = request.session['user']
    formdata = Drafts.objects.filter(createdBy=user)
    if request.method == 'POST' and 'createTask' not in list(request.POST) and 'discard' not in list(request.POST):
        taskid = request.POST.get('taskId')
        taskdata = Drafts.objects.filter(taskId=taskid)
        return render(request, 'TaskManagement/editandsubmit.html',{'user':user,'taskdata':taskdata})
    elif request.method =='POST' and 'createTask' in list(request.POST):
        print('in here')
        taskdata = Drafts.objects.get(taskId=request.POST.get('taskId'))
        task = Tasks()
        task.taskId = request.POST.get('taskId')
        task.taskName = request.POST.get('taskName')
        task.taskDescription = request.POST.get('description')
        task.assignedTo = taskdata.assignedTo
        task.remarks = taskdata.remarks
        task.createdBy = user
        task.lastModifiedBy = user
        task.assignedTo = taskdata.assignedTo
        task.createdDate = taskdata.createdDate
        task.save()
        taskdata.delete()
        return createdByMe(request)
    elif request.method =='POST' and 'discard' in list(request.POST):
        taskdata = Drafts.objects.get(taskId=request.POST.get('taskId'))
        taskdata.delete()
        return showdrafts(request)
    else:
        print('error')

    return render(request, 'TaskManagement/editandsubmit.html', {'user':user,'formdata':formdata})

@login_required
def discard(request):
    user = request.session['user']
    formdata = Drafts.objects.filter(createdBy=user)
    if request.method == 'POST' and 'deleteTask' not in list(request.POST):
        taskid = request.POST.get('taskId')
        taskdata = Drafts.objects.filter(taskId=taskid)
        return render(request, 'TaskManagement/delete.html',{'user':user,'taskdata':taskdata})
    elif request.method =='POST' and 'deleteTask' in list(request.POST):
        print('in here')
        taskdata = Drafts.objects.get(taskId=request.POST.get('taskId'))
        taskdata.delete()
        return showdrafts(request)
    return render(request,'TaskManagement/delete.html',{'user':user,'formdata':formdata})

@login_required
def exportcreated(request):
    user = request.session['user']
    state=''
    if request.method == 'POST' and 'created' in list(request.POST):
        tasks = Tasks.objects.filter(createdBy=user)
        state='createdBy'+str(user)
    elif request.method == 'POST' and 'assigned' in list(request.POST):
        tasks = Tasks.objects.filter(assignedTo=user)
        state='Assignedto'+str(user)
    elif request.method == 'POST' and 'drafts' in list(request.POST):
        tasks = Drafts.objects.filter(createdBy=user)
        state='DraftsCreatedBy'+str(user)
    elif request.method =='POST' and 'all' in list(request.POST):
        tasks = Tasks.objects.all()
        state='allTasks'+str(user)
    else:
        tasks= Tasks.objects.all()
    df = tasks.to_dataframe()
    date =datetime.datetime.now()
    formateddate = str(date.year)+str(date.month)+str(date.day)
    filename = 'CSVfile'+state+formateddate+'.csv'
    df.to_csv(settings.MEDIA_ROOT+'/'+filename)
    file_path = settings.MEDIA_ROOT +'/'+ filename
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename='+filename

    return response


    # return homePage(request)
