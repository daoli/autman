from django.contrib.auth.decorators import user_passes_test
from django.conf.urls import patterns, url
from reservation.views import ReservationView
# from reservation.views import reserve


staff_required = user_passes_test(lambda u: u.is_staff)

urlpatterns = patterns('',
    # url(r'^lunch/', staff_required(reserve)),

    url(r'^$', ReservationView.as_view(),
        name="reservation"),
)
