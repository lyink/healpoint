from django.db import models
# import programs from APP1
from APP1.models import Programs as Programs_from_App1

class Registration(models.Model):
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    resident=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    email=models.CharField(max_length=200,primary_key=True)
    tutorial_session=models.TextField(max_length=250)
    accomodation=models.TextField(max_length=250)
    disability=models.TextField(max_length=250)
    certificate=models.TextField(max_length=250)
    marital=models.CharField(max_length=200)
    passport_size=models.ImageField(upload_to='application_passports/')
    certificates=models.FileField(upload_to='application_certificates/')
    date_of_birth=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    message=models.TextField()
    program=models.ForeignKey(Programs_from_App1,on_delete=models.CASCADE)
    
class MessageToForm(models.Model):
    message=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    closed_date=models.DateField()
