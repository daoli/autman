from django.contrib.auth.decorators import user_passes_test
from django.conf.urls import patterns, url
from reservation.views import ChargeHistoryView, ReservationView, login_user
# from reservation.views import reserve
from django.contrib.auth.decorators import login_required

staff_required = user_passes_test(lambda u: u.is_staff)

urlpatterns = patterns('',
    url(r'^$', login_required(ReservationView.as_view()),
        name="reservation"),
    url(r'^history/$', login_required(ChargeHistoryView.as_view()),
        name="history"),
    url(r'^login/$', login_user, name='login'),
)
