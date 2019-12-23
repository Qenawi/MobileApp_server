from django.urls import path
from . import views
app_name='Api'




urlpatterns = [

    path('login/',views.login_API,name='login_Api'),
    path('logout/', views.logut_API, name='logout'),
    path('note/',views.Not_id,name='note_id'),
    path('meeting/',views.Meeting_API,name='meeting_Api'),
    path('new/',views.new_meeting,name='new_meeting'),
    path('list/',views.list_of_users,name='list'),
    path('register/',views.Register_API,name='register'),
    path('message/', views.send_message, name='send')


]