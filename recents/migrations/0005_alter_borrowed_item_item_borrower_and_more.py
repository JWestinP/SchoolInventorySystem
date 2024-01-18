# Generated by Django 4.1.7 on 2023-12-27 09:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recents', '0004_borrowed_item_item_borrower'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowed_item',
            name='item_borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='borrowed_item',
            name='item_photo',
            field=models.ImageField(blank=True, upload_to='borrowed_item'),
        ),
    ]