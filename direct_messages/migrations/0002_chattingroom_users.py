# Generated by Django 3.2.13 on 2023-12-23 03:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('direct_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chattingroom',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
