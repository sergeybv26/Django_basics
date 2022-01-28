from django.db import models
from django.db.models import F

from mainapp.models import Product


class Report(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество покупок')

    @staticmethod
    def get_items():
        return Report.objects.filter(quantity__gt=0).order_by('quantity')
