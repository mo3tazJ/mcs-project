# Generated by Django 5.1.2 on 2024-11-04 12:07

import model_utils.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_service_rejected_at_alter_service_started_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='approved_at',
            field=model_utils.fields.MonitorField(blank=True, default=None, monitor='state', null=True, when={'approved'}),
        ),
        migrations.AlterField(
            model_name='service',
            name='archived_at',
            field=model_utils.fields.MonitorField(blank=True, default=None, monitor='state', null=True, when={'archived'}),
        ),
        migrations.AlterField(
            model_name='service',
            name='closed_at',
            field=model_utils.fields.MonitorField(blank=True, default=None, monitor='state', null=True, when={'closed'}),
        ),
        migrations.AlterField(
            model_name='service',
            name='ended_at',
            field=model_utils.fields.MonitorField(blank=True, default=None, monitor='state', null=True, when={'ended'}),
        ),
    ]
