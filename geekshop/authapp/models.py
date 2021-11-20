from datetime import timedelta, datetime

import pytz
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='Аватарка')
    age = models.PositiveIntegerField(verbose_name='возраст')

    activation_key = models.CharField(max_length=128, verbose_name='ключ активации', blank=True, null=True)
    activation_key_expired = models.DateTimeField(blank=True, null=True)

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activation_key_expired + timedelta(hours=48):
            return True
        else:
            return False

    def activate_user(self):
        self.is_active = True
        self.activation_key = None
        self.activation_key_expired = None
        self.save()
