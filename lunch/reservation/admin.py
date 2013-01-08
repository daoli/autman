from django.contrib import admin
from reservation.models import Reservation
from reservation.models import UserProfile
from reservation.forms import ReservationForm


class ReservationAdmin(admin.ModelAdmin):
    list_filter = ['date']


class UserProfileAdmin(admin.ModelAdmin):
    form = ReservationForm
    list_display = (
                    'user',
                    'balance',
                    )
    readonly_fields = ('balance',)

    def save_model(self, request, obj, form, change):
        if form and form.cleaned_data['recharge_amount']:
            recharge_amount = int(form.cleaned_data['recharge_amount'])
            obj.balance += recharge_amount

        obj.save()

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
