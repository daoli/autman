from django.db import models
from django.contrib.auth.models import User


class Reservation(models.Model):
	user = models.ForeignKey(User)
	date = models.DateField(auto_now_add=True)


class UserProfile(models.Model):
	user = models.ForeignKey(User)
	balance = models.IntegerField(default=0)
