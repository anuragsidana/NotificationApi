# Generated by Django 2.0.1 on 2018-04-01 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('message', models.CharField(max_length=250)),
                ('date', models.CharField(max_length=20)),
                ('time', models.DateTimeField(max_length=20)),
                ('task_id', models.CharField(blank=True, editable=False, max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nots', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User_Id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
