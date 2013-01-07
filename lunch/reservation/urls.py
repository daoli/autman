from django.conf.urls import patterns, url
from reservation.views import ReservationView

urlpatterns = patterns('',
    url(r'^$', ReservationView.as_view(),
        name="reservation"),
)
