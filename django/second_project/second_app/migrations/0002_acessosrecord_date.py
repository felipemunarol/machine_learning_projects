# Generated by Django 3.2.22 on 2024-06-17 00:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('second_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='acessosrecord',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
