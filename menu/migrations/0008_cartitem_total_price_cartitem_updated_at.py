# Generated by Django 4.1.3 on 2023-05-06 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_orderitem_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
