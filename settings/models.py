from django.db import models
from django.contrib.auth.models import User # to settings.py ???
from django.db.models.signals import post_save
from django.conf import settings


class UserTimeZone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone_field = models.CharField(max_length=100, default=settings.TIME_ZONE, help_text='Make sure you write the time zone correctly')

    def __str__(self):
        return f'{self.user} - {self.timezone_field}'


class UserSalesShowing(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_show = models.BooleanField(default=True)
    client_name_show = models.BooleanField(default=True)
    client_address_show = models.BooleanField(default=True)
    manager_show = models.BooleanField(default=True)
    date_created_show = models.BooleanField(default=True)
    date_updated_show = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username}'


# from django.dispatch import receiver
# @receiver(post_save, sender=User)
def create_UserSalesShowing(instance, created, *args, **kwargs):
    if created:
        UserSalesShowing.objects.create(user=instance)
        UserTimeZone.objects.create(user=instance)
post_save.connect(receiver=create_UserSalesShowing, sender=User)