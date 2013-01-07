from django.contrib import admin
from reservation.models import Reservation
from reservation.models import UserProfile

admin.site.register(Reservation)
admin.site.register(UserProfile)
