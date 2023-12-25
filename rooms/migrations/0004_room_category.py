# Generated by Django 3.2.13 on 2023-12-23 01:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('rooms', '0003_alter_amenity_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.category'),
        ),
    ]
