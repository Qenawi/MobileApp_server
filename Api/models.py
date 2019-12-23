from django.db import models
from phonenumber_field.modelfields import PhoneNumberField




class user(models.Model):
    Name=models.CharField(max_length=20,default='')
    Username=models.CharField(max_length=20,blank=False,unique=True,default='')
    Password=models.CharField(max_length=50,default='')
    Position=models.CharField(max_length=50,default='')
    Mobile_Number=PhoneNumberField(max_length=13,unique=True,blank=False,region='EG',help_text="Enter a valid phone number (e.g. +201*********)",)
    Note_ID=models.TextField(max_length=200,blank=True,null=True,default='')
    def __str__(self):
        return self.Name





class meeting(models.Model):
    H='High'
    M="Medium"
    L="Low"
    pr = [(H,'High'),
          (M,'Medium'),
          (L,'Low')]
    title=models.CharField(max_length=50,unique=True)
    date=models.DateField()
    time=models.TimeField()
    location_address=models.CharField(max_length=100)
    location_lat=models.CharField(max_length=50,blank=True,null=True)
    location_long = models.CharField(max_length=50,blank=True,null=True)
    subject=models.CharField(max_length=50)
    priority=models.CharField(max_length=20,choices= pr,default='Low')
    username=models.ManyToManyField(user)
    def __str__(self):
        return self.title


class Notification(models.Model):
    title=models.CharField(max_length=50)
    subject=models.CharField(max_length=50)
    user=models.CharField(max_length=25)
    def __str__(self):
        return self.title


