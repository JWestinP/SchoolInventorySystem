# Generated by Django 4.1.7 on 2023-12-18 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Borrowed_Items',
            fields=[
                ('item_id', models.IntegerField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=128)),
                ('item_quantity', models.IntegerField()),
                ('item_returned', models.BooleanField()),
                ('item_date_borrowed', models.DateField()),
                ('item_date_returned', models.DateField(blank=True)),
            ],
        ),
    ]
