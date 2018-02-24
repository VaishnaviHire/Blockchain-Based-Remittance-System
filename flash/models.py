from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User
from django.db import models


# Create your models here.

class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    genre = models.CharField(max_length=100)
    logo = models.CharField(max_length=1000)

    def __str__(self):
        return self.artist + "-" + self.genre

class Song(models.Model):
     album = models.ForeignKey(Album, on_delete=models.CASCADE)
     file_type = models.CharField(max_length=10)
     title = models.CharField(max_length=100)

     def __str__(self):
         return self.title

class Lists(models.Model):
    user = models.ForeignKey(User, default=1)
    amount = models.CharField(max_length=400)
    recipient = models.CharField(max_length=30)

    def __str__(self):
        return self.amount

class Position(models.Model):
    user = models.ForeignKey(User, default=1)
    latitude = models.CharField(max_length=20, default=19.1239)
    longitude = models.CharField(max_length=20, default=72.8361)


    def __str__(self):
        return self.user.username

class Notification(models.Model):
    user = models.ForeignKey(User, default=1)
    store_name = models.CharField(max_length=100)
    store_latitude = models.CharField(max_length=20,default=19.1239)
    store_longitude = models.CharField(max_length=20, default=72.8361)

    def __str__(self):
        return self.store_name

class Transfer(models.Model):
    username = models.ForeignKey(User, default=1)
    amount = models.CharField(max_length=40, default=1)
    recipient = models.CharField(max_length=300, default=1)

    def __str__(self):
        return self.amount


class AddToWallet(models.Model):
    user = models.ForeignKey(User, default=1)
    amount = models.CharField(max_length=20, default=0)
    CHOICES = (('usd', 'usd'), ('inr', 'inr'), ('btc', 'btc'), ('eur', 'eur'))
    currency = models.CharField(max_length=5, choices=CHOICES)


    def __str__(self):
        return self.user.username

