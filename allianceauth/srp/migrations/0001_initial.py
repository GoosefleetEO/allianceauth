# Generated by Django 1.10.1 on 2016-09-05 21:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eveonline', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SrpFleetMain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fleet_name', models.CharField(default=b'', max_length=254)),
                ('fleet_doctrine', models.CharField(default=b'', max_length=254)),
                ('fleet_time', models.DateTimeField()),
                ('fleet_srp_code', models.CharField(default=b'', max_length=254)),
                ('fleet_srp_status', models.CharField(default=b'', max_length=254)),
                ('fleet_srp_aar_link', models.CharField(default=b'', max_length=254)),
                ('fleet_commander', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eveonline.EveCharacter')),
            ],
        ),
        migrations.CreateModel(
            name='SrpUserRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('killboard_link', models.CharField(default=b'', max_length=254)),
                ('after_action_report_link', models.CharField(default=b'', max_length=254)),
                ('additional_info', models.CharField(default=b'', max_length=254)),
                ('srp_status', models.CharField(default=b'', max_length=254)),
                ('srp_total_amount', models.BigIntegerField(default=0)),
                ('kb_total_loss', models.BigIntegerField(default=0)),
                ('srp_ship_name', models.CharField(default=b'', max_length=254)),
                ('post_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eveonline.EveCharacter')),
                ('srp_fleet_main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='srp.SrpFleetMain')),
            ],
        ),
    ]
