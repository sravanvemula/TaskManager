from django.contrib import admin
from TaskManagement.models import UserProfileInfo,Status,Tasks,Drafts
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Status)
admin.site.register(Tasks)
admin.site.register(Drafts)
