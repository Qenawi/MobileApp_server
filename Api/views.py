from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import time
from .models import user
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from . import models
from passlib.hash import pbkdf2_sha256
from .json import json_user
from fcm_django.models import FCMDevice


@csrf_exempt
def Register_API(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Name = data.get('Name', None)
        Username = data.get('Username', None)
        Password = data.get('Password', None)
        Phone_Number = data.get('PhoneNumber', None)
        Position = data.get('Position', None)
        Note_ID = data.get('Note_ID', None)
        try:
            ops = models.user.objects.create(Name=Name, Username=Username, Password=Password,
                                             Mobile_Number=Phone_Number, Position=Position, Note_ID=Note_ID)
            ops.save()
            ops2 = FCMDevice.objects.create(name=Username, registration_id=Note_ID, type='android')
            ops2.save()
            ops1 = models.user.objects.get(Username=Username)
            phone = str(ops1.Mobile_Number)
            User_Data = {'username': ops1.Username, 'name': ops1.Name, 'Mobile_Number': phone,
                         'position': ops1.Position}
            return JsonResponse(User_Data)
        except:
            return HttpResponse('Error')
    else:
        return HttpResponse("request method not allowed")


@csrf_exempt
def login_API(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Username = data.get('Username', None)
        Password = data.get('Password', None)
        Note_ID = data.get('Note_ID', None)
        try:
            ops = models.user.objects.get(Username=Username, Password=Password)
            ops1 = FCMDevice.objects.get(name=Username)
            if Note_ID != '':
                ops.Note_ID = Note_ID
                ops.save()
                ops1.registration_id = Note_ID
                ops1.save()
                phone = str(ops.Mobile_Number)
                user_data = {'username': ops.Username, 'name': ops.Name, 'Mobile_Number': phone,
                             'position': ops.Position}
                return JsonResponse(user_data)
            else:
                phone = str(ops.Mobile_Number)
                user_data = {'username': ops.Username, 'name': ops.Name, 'Mobile_Number': phone,
                             'position': ops.Position}
                return JsonResponse(user_data)
        except:
            return HttpResponse("wrrong Username")
    else:
        return HttpResponse("request method not allowed")


@csrf_exempt
def logut_API(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Username = data.get('Username', None)
        ops = FCMDevice.objects.get(name=Username)
        ops1 = models.user.objects.get(Username=Username)
        try:
            ops1.Note_ID = ''
            ops1.save()
            ops.registration_id = ''
            ops.save()
            return HttpResponse("Done")
        except:
            pass
    else:
        return HttpResponse("request method not allowed")


@csrf_exempt
def Not_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Username = data.get('Username', None)
        Note_ID = data.get('Note_ID', None)
        try:
            ops = models.user.objects.get(Username=Username)
            ops.Note_ID = Note_ID
            ops.save()
            time.sleep(0.200)
            return HttpResponse("Done")
        except:
            return HttpResponse('Not Found')

    else:
        return HttpResponse('request method not allowed')


@csrf_exempt
def Meeting_API(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Username = data.get('Username', None)
        try:
            ops = models.user.objects.get(Username=Username)
            user_id = ops.id  # get User Id
            ops2 = models.meeting.username.through.objects.filter(user_id=user_id)
            ops4 = []
            for query in ops2:
                meeting_id = query.meeting_id
                ops3 = models.meeting.objects.filter(id=meeting_id)
                ops4 += ops3
                data = serializers.serialize('json', ops4,
                                             fields=('title', "date", "time", "location_address", "subject", "priority"

                                                     ))
            return HttpResponse(data)
        except:
            return HttpResponse("Not Found")
    else:
        return HttpResponse('request method not allowed')


@csrf_exempt
def new_meeting(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title', None)
        date = data.get('date', None)
        time = data.get('time', None)
        location_address = data.get('location_address', None)
        location_lat = data.get('location_lat', None)
        location_long = data.get('location_long', None)
        subject = data.get('subject', None)
        priority = data.get('priority', None)
        username = data.get('username', None)
        print(data)
        try:
            ops = models.meeting.objects.create(title=title, date=date, time=time,
                                                location_address=location_address, location_lat=location_lat,
                                                location_long=location_long, subject=subject, priority=priority)

            for name in username:
                ops1 = models.user.objects.get(Username=name)
                ops2 = models.meeting.objects.get(title=title)
                ops3 = models.meeting.username.through.objects.create(meeting_id=ops2.id, user_id=ops1.id)
                ops3.save()
            ops.save()
            show_info = {'titlt': ops2.title, 'id': ops2.id}
            print(show_info)
            return JsonResponse(show_info)
        except:
            print("please make meeting name unique or check User")
            return HttpResponse("please make meeting name unique or check User")
    else:
        return HttpResponse('request method not allowed')


def list_of_users(request):
    if request.method == 'GET':
        try:
            ops = models.user.objects.all()
            data = serializers.serialize('json', ops, fields=('id', 'Mobile_Number', 'Name', 'Username'))
            time.sleep(0.200)
            return HttpResponse(data)
        except:
            return HttpResponse("Error")

    else:
        return HttpResponse('request method not allowed')


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        meeting_id = data.get('meeting_id', None)
        title = data.get('title', None)
        message = data.get('message', None)
        try:
            get_meetings = models.meeting.username.through.objects.filter(
                meeting_id=meeting_id)  # get_meeting_id __to_get_user_id
            for name in get_meetings:
                ops1 = models.user.objects.get(id=name.user_id)
                ops2 = FCMDevice.objects.get(name=ops1.Username)
                ops2.send_message(data={"title": title,
                                        "body": message})
            return HttpResponse("Done")
        except:
            return HttpResponse("ERROR")
    else:
        return HttpResponse('request method not allowed')
