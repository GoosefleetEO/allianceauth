# Generated by Django 3.1.13 on 2021-10-12 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eveonline', '0014_auto_20210105_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='EveFactionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faction_id', models.PositiveIntegerField(db_index=True, unique=True)),
                ('faction_name', models.CharField(max_length=254, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='evecharacter',
            name='faction_id',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='evecharacter',
            name='faction_name',
            field=models.CharField(blank=True, default='', max_length=254, null=True),
        ),
        migrations.AddIndex(
            model_name='evecharacter',
            index=models.Index(fields=['faction_id'], name='eveonline_e_faction_d5274e_idx'),
        ),
    ]