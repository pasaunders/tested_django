"""Routes for managing user travel."""

from django.conf.urls import url
from .views import ListTrips, TripDetail, NewTrip, JoinTrip

urlpatterns = [
    url(r'^$', ListTrips.as_view(), name='list'),
    url(r'^destination/(?P<pk>[0-9]+)/$', TripDetail.as_view(), name='detail'),
    url(r'^add/$', NewTrip.as_view(), name='add'),
    url(r'^join/(?P<pk>[0-9]+)/$', JoinTrip.as_view(), name='join'),
]
