# Generated by Django 4.0.3 on 2022-03-19 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('famsafe', '0002_alter_uploadfile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
