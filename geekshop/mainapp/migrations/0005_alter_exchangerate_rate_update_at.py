# Generated by Django 3.2.8 on 2021-12-19 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_exchangerate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangerate',
            name='rate_update_at',
            field=models.DateField(auto_now=True, verbose_name='обновлен'),
        ),
    ]
