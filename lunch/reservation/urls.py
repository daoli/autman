from django.contrib.auth.decorators import user_passes_test
from django.conf.urls import patterns, url
from reservation.views import ReservationView
# from reservation.views import reserve
from django.contrib.auth.decorators import login_required

staff_required = user_passes_test(lambda u: u.is_staff)

urlpatterns = patterns('',
    url(r'^$', login_required(ReservationView.as_view()),
        name="reservation"),
)
