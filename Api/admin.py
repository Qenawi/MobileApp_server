from django.contrib import admin
from .models import meeting,user,Notification

class User_Display(admin.ModelAdmin):
    list_display = ['Name','Username']




admin.site.register(user,User_Display)
admin.site.register(meeting)
admin.site.register(Notification)
