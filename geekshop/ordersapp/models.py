from django.conf import settings
from django.db import models

from mainapp.models import Product

#
# class OrderItemQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         for _object in self:
#             _object.product.quantity += _object.quantity
#             _object.product.save()
#         super().delete(*args, **kwargs)


class Order(models.Model):
    STATUS_FORMING = 'FM'
    STATUS_SENT_TO_PROCEED = 'STP'
    STATUS_PROCEEDED = 'PRD'
    STATUS_PAID = 'PD'
    STATUS_READY = 'RDY'
    STATUS_CANCEL = 'CNC'

    STATUSES = (
        (STATUS_FORMING, 'Формируется'),
        (STATUS_SENT_TO_PROCEED, 'Отправлен на обработку'),
        (STATUS_PROCEEDED, 'Обработан'),
        (STATUS_PAID, 'Оплачен'),
        (STATUS_READY, 'Готов'),
        (STATUS_CANCEL, 'Отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(verbose_name='статус', max_length=3, choices=STATUSES, default=STATUS_FORMING)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='обновлен')
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Текущий заказ:'.format(self.id)

    def get_total_quantity(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, _items)))

    def get_total_cost(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.product_cost, _items)))

    def delete(self, *args, **kwargs):
        for _item in self.orderitems.select_related():
            _item.product.quantity += _item.quantity
            _item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')
    # objects = OrderItemQuerySet.as_manager()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)
