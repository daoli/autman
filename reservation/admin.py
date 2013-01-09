from django.contrib import admin
from reservation.models import RechargeHistory
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
    readonly_fields = (
                       'balance',
                       )

    def save_model(self, request, obj, form, change):
        if form and form.cleaned_data['recharge_amount']:
            recharge_amount = int(form.cleaned_data['recharge_amount'])
            obj.balance += recharge_amount
            admin = request.user
            RechargeHistory.objects.create(user=obj.user,
                                           admin=admin,
                                           recharge_amount=recharge_amount)

        obj.save()


class RechargeHistoryAdmin(admin.ModelAdmin):
    list_display = (
                    'user',
                    'recharge_amount',
                    'admin',
                    'datetime',
                    )
    readonly_fields = ('user',
                       'recharge_amount',
                       'admin',
                       'datetime',
                       )


admin.site.register(RechargeHistory, RechargeHistoryAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
