# Generated by Django 3.0.5 on 2020-07-21 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_complete',
            field=models.BooleanField(default=False),
        ),
    ]
