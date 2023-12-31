# Generated by Django 3.2.13 on 2023-12-23 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0004_room_category'),
        ('experiences', '0002_auto_20231223_0121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='')),
                ('experience', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='experiences.experience')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.ImageField(upload_to='')),
                ('description', models.CharField(max_length=140)),
                ('experience', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='experiences.experience')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rooms.room')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
