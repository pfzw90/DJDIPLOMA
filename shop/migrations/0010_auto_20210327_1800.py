# Generated by Django 3.1.2 on 2021-03-27 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20210327_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsorders',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
        ),
    ]
