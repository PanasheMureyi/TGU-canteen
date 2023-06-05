# Generated by Django 4.1.3 on 2023-06-04 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0016_menuitem_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='menu_item_images')),
            ],
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='image',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='images',
            field=models.ManyToManyField(blank=True, to='menu.image'),
        ),
    ]
