from django.db import models

class Daneshjoo(models.Model):
    name = models.CharField(max_length=200,unique=True)
    gender_choice = (
        ("male" , "male"),
        ("female" , "female"),
    )
    gender = models.CharField(max_length=200,default="male",choices=gender_choice)

class Friend(models.Model):
    daneshjoo = models.ForeignKey(Daneshjoo , on_delete=models.CASCADE)
    friend = models.ForeignKey(Daneshjoo , on_delete=models.CASCADE)
