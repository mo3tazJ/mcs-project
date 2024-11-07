# Generated by Django 5.1.2 on 2024-11-06 08:00

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mobile', models.CharField(max_length=25, verbose_name='Mobile No.')),
                ('about', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updatet_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='backend.department', verbose_name='Department')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='backend.role', verbose_name='Role')),
            ],
            options={
                'verbose_name': 'Employee User',
                'verbose_name_plural': 'Employee Users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='device',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices', to='backend.employee', verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='service',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='empservices', to='backend.employee', verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='service',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wrkservices', to='backend.employee', verbose_name='Worker'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
