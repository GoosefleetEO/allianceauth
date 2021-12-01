# Generated by Django 1.10.2 on 2016-12-12 03:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmfUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='smf', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(max_length=254)),
            ],
        ),
    ]
