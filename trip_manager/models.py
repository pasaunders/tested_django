from django.db import models
from django.contrib.auth.models import User


class Trip(models.Model):
    planner = models.ForeignKey(
        User,
        related_name='trips',
    )
    guests = models.ManyToManyField(
        User,
        related_name='guest_trips',
        blank=True,
    )
    destination = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    date_from = models.DateField()
    date_to = models.DateField()