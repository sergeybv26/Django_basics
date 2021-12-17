from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q, F, When, Case, IntegerField, DecimalField

from mainapp.models import Product
from adminapp.views import db_profile_by_type
from ordersapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        # test_products = Product.objects.filter(Q(category__name='офис') | Q(category__name='модерн')).select_related()
        #
        # print(test_products)
        #
        # db_profile_by_type('learn_db', '', connection.queries)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.05

        action_1_delta = timedelta(hours=12)
        action_2_delta = timedelta(days=1)

        action_1 = 1
        action_2 = 2
        action_3 = 3

        action_1_condition = Q(order__updated_at__lte=F('order__created_at') + action_1_delta)
        action_2_condition = Q(order__updated_at__gt=F('order__created_at') + action_1_delta) &\
            Q(order__updated_at__lte=F('order__created_at') + action_2_delta)
        action_3_condition = Q(order__updated_at__gt=F('order__created_at') + action_2_delta)

        action_1_order = When(action_1_condition, then=action_1)
        action_2_order = When(action_2_condition, then=action_2)
        action_3_order = When(action_3_condition, then=action_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * action_2_discount)
        action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1_order,
                action_2_order,
                action_3_order,
                output_field=IntegerField(),
            )
        ).annotate(
            total_price=Case(
                action_1_price,
                action_2_price,
                action_3_price,
                output_field=DecimalField(),
            )
        ).order_by('action_order', 'total_price').select_related()

        for orderitem in test_orders:
            print(f'{orderitem.action_order:2}: заказ № {orderitem.pk:3}: '
                  f'{orderitem.product.name:15}: скидка {abs(orderitem.total_price):6.2f} руб. |'
                  f' {orderitem.order.updated_at - orderitem.order.created_at}')
