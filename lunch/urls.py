from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^lunch/', include('reservation.urls', 'resv', 'resv')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', lambda x: HttpResponseRedirect(reverse('resv:reservation')))
)
