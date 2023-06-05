# Generated by Django 4.1.3 on 2023-06-04 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0017_image_remove_menuitem_image_menuitem_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='images',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='menu_item_images'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]