# Generated by Django 3.1 on 2020-08-14 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_auto_20200814_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='history',
        ),
    ]
