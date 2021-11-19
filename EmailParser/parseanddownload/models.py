from django.db import models

# Create your models here.
class TalksData(models.Model):
    Sender=models.TextField(max_length=100,blank=True)
    Subject=models.TextField(max_length=200,blank=True)
    DateofEmail=models.TextField(max_length=50,blank=True)
    Message_body=models.TextField(max_length=1000,blank=True)
    Speaker=models.TextField(max_length=200,blank=True)
    Topic=models.TextField(max_length=300,blank=True)
    Time=models.TextField(max_length=30,blank=True)
    DateofWorkshop=models.TextField(max_length=20,blank=True)
    Venue=models.TextField(max_length=30,blank=True)

    class Meta:
    	unique_together=["Sender","Subject","DateofEmail","DateofWorkshop","Message_body","Venue","Time","DateofWorkshop","Topic"]