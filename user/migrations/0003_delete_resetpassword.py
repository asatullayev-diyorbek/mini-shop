# Generated by Django 5.0.1 on 2024-10-01 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_resetpassword'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ResetPassword',
        ),
    ]
