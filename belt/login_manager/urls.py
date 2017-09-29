"""Routes for managing user login and registration."""

from django.conf.urls import url
from .views import SignIn, logout_view


urlpatterns = [
    url(r'^$', SignIn.as_view(), name='signin'),
    url(r'^logout$', logout_view.as_view(), name='logout')
]
