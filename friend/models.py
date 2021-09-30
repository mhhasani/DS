from django.db import models

class Daneshjoo(models.Model):
    name = models.CharField(max_length=200,unique=True)

class Friend(models.Model):
    daneshjoo = models.ForeignKey(Daneshjoo , on_delete=models.CASCADE,related_name="daneshjoo")
    friend = models.ManyToManyField(Daneshjoo,related_name="friend")
