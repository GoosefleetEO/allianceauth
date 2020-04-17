# Generated by Django 2.2.10 on 2020-03-21 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_nameformatter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nameformatconfig',
            name='format',
            field=models.CharField(help_text='For information on constructing name formats please see the official documentation, topic "Services Name Formats".', max_length=100),
        ),
    ]