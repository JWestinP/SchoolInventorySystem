# Generated by Django 4.1.7 on 2023-12-21 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recents', '0002_rename_borrowed_items_borrowed_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowed_item',
            name='item_photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]