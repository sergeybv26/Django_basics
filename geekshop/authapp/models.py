from datetime import timedelta, datetime

import pytz
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='Аватарка')
    avatar_url = models.CharField(max_length=512, blank=True, null=True, verbose_name='Ссылка на аватарку')
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)

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


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    OTHER = 'O'

    GENDERS = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
        (OTHER, 'Не указан')
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(max_length=128, verbose_name='теги', blank=True)
    about_me = models.TextField(max_length=512, verbose_name='обо мне', blank=True)
    gender = models.CharField(choices=GENDERS, default=OTHER, verbose_name='пол', max_length=1)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def update_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
