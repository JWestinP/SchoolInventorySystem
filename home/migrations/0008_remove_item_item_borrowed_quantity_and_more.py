# Generated by Django 4.1.7 on 2023-12-29 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_category_item_delete_cleaning_material_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='item_borrowed_quantity',
        ),
        migrations.RemoveField(
            model_name='item',
            name='item_current_quantity',
        ),
        migrations.RemoveField(
            model_name='item',
            name='item_total_quantity',
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_total_quantity', models.IntegerField()),
                ('item_current_quantity', models.IntegerField()),
                ('item_borrowed_quantity', models.IntegerField()),
                ('item_information', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.item')),
            ],
        ),
    ]