# Generated by Django 2.2.5 on 2019-12-16 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='category',
        ),
        migrations.RemoveField(
            model_name='note',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Note',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
