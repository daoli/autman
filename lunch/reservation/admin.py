from django.contrib import admin
from reservation.models import Reservation
from reservation.models import UserProfile

class ReservationAdmin(admin.ModelAdmin):
	list_filter = ['date']

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(UserProfile)
