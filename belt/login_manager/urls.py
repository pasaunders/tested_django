"""Routes for managing user login and registration."""

from django.conf.urls import url
from .views import index, signin, logout_view


urlpatterns = [
    url(r'^$', index.as_view(), name='home'),
    url(r'^signin$', signin.as_view(), name='signin'),
    url(r'^logout$', logout_view.as_view(), name='logout')
]
