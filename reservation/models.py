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


class RechargeHistory(models.Model):
    user = models.ForeignKey(User, related_name='user')
    admin = models.ForeignKey(User, related_name='admin')
    recharge_amount = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        name = self.user.first_name if self.user.first_name else self.user.username
        admin = self.admin.first_name if self.admin.first_name else self.admin.username
        return "%s charged CNY %s at %s by %s" % (name,
                self.recharge_amount, self.datetime, admin)

    class Meta:
        verbose_name_plural = "recharge history"
