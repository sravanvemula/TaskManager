from django import forms
from django.core import validators
from django.contrib.auth.models import User
from TaskManagement.models import UserProfileInfo,Tasks

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        help_texts = {
        'username' : None,
        }

class CreateNewTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        exclude=['createdBy','lastModifiedBy','assignedTo','taskId','status']
        widgets = {
          'taskDescription': forms.Textarea(attrs={'rows':4, 'cols':50}),
          'remarks': forms.Textarea(attrs={'rows':4,'cols':50}),
        }

class selectUserForm(forms.Form):
    Assignto = forms.ModelChoiceField(queryset=User.objects.all())

class selectTaskForm(forms.ModelForm):
    # TaskId = forms.ModelChoiceField(queryset=Tasks.objects.all())
    # def __init__(self, user, *args, **kwargs):
    #     super(selectTaskForm, self).__init__(*args, **kwargs)
    #     self.fields['TaskId'].queryset = Tasks.objects.filter(assignedTo=user)
    class Meta:
        model = Tasks
        fields = ('status','remarks')
        widgets = {
          'remarks': forms.Textarea(attrs={'rows':4,'cols':50}),
        }

class TasksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TasksForm, self).__init__(*args, **kwargs)
        self.fields['taskId','taskId','taskDescription','createdDate','createdBy','assignedTo',
        'lastModifiedDate','lastModifiedBy',].disabled = True
    class Meta:
        model = Tasks
        fields='__all__'

class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('status','remarks')
