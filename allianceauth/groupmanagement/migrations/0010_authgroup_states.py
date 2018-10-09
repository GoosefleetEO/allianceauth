# Generated by Django 2.0.6 on 2018-07-11 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_ownershiprecord'),
        ('groupmanagement', '0008_remove_authgroup_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='authgroup',
            name='states',
            field=models.ManyToManyField(blank=True, help_text='States listed here will have the ability to join this group provided they have the proper permissions.', related_name='valid_states', to='authentication.State'),
        ),
    ]
