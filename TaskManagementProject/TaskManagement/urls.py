from django.conf.urls import url
from TaskManagement import views

app_name = 'TaskManagement'

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^userLogin/', views.userLogin, name='userLogin'),
    url(r'^logout/', views.userLogout, name='userLogout'),
    url(r'^homePage/',views.homePage, name='homePage'),
    url(r'^assignedtome/',views.assignedToMe, name='assignedtome'),
    url(r'^createdbyme/',views.createdByMe, name='createdbyme'),
    url(r'^createNewTask/',views.createNewTask,name='createNewTask'),
    url(r'^updateTask/', views.updateTask, name='updateTask'),
    url(r'^drafts/',views.showdrafts,name='drafts'),
    url(r'^editAndSubmit/',views.editAndSubmit,name='editAndSubmit'),
    url(r'^discard/',views.discard,name='discard'),
    url(r'^indexhome/',views.indexhome,name='indexhome'),
]
