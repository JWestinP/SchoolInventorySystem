# Generated by Django 4.1.7 on 2023-12-20 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cleaning_Materials',
            new_name='Cleaning_Material',
        ),
        migrations.RenameModel(
            old_name='Rooms',
            new_name='Room',
        ),
    ]
