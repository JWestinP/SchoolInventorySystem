# Generated by Django 4.1.7 on 2023-12-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recents', '0006_alter_borrowed_item_item_borrower'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowed_item',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='borrowed_item',
            name='item_id',
            field=models.IntegerField(),
        ),
    ]
