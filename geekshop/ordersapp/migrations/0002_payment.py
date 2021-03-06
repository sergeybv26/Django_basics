# Generated by Django 3.2.8 on 2021-12-20 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ik_am', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма платежа')),
                ('ik_desc', models.CharField(max_length=128, verbose_name='Описание платежа')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordersapp.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
