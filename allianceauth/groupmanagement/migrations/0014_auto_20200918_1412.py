# Generated by Django 3.1.1 on 2020-09-18 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupmanagement', '0013_fix_requestlog_date_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestlog',
            name='request_type',
            field=models.BooleanField(null=True),
        ),
    ]
