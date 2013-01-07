from django.contrib.auth.decorators import user_passes_test
from reservation.views import reserve
from django.conf.urls import patterns, url

staff_required = user_passes_test(lambda u: u.is_staff)

urlpatterns = patterns('',
    url(r'^lunch/', staff_required(reserve)),
)
