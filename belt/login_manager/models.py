import re
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver
from django.db.models.signals import post_save, post_migrate

class User_valid(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if not re.match(r'^\D+', postData['first_name']):
            errors['name'] = 'Name may not include digits.'
        if not re.match(r'^\D+', postData['last_name']):
            errors['name'] = 'Name may not include digits.'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Password must match password confirmation.'
        if len(User.objects.filter(email=postData['email'])):
            errors['email'] = 'Email must be unique.'
        return errors


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
        )
    objects = User_valid()

    class Meta:
        permissions = (
            ('admin', 'Access to admin pages'),
            ('user', 'all normal users')
        )

@receiver(post_save, sender=User)
def make_profile_for_user(sender, instance, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=instance)
