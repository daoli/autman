from django.db import models
from django.contrib.auth.models import User


class Reservation(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        name = self.user.first_name if self.user.first_name else self.user.username
        return name + ' on ' + str(self.date)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    balance = models.IntegerField(default=0)

    def __unicode__(self):
        name = self.user.first_name if self.user.first_name else self.user.username
        return name
