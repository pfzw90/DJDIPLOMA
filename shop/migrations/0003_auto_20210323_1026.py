# Generated by Django 3.1.2 on 2021-03-23 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210323_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='heading',
            field=models.TextField(default='default', verbose_name='Заголовок'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collection',
            name='text',
            field=models.TextField(default='default', verbose_name='Описание'),
            preserve_default=False,
        ),
    ]