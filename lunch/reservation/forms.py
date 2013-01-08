from django.forms import ModelForm
from django import forms
from reservation.models import UserProfile


class ReservationForm(ModelForm):
    recharge_amount = forms.IntegerField(required=False)

    class Meta:
        model = UserProfile
