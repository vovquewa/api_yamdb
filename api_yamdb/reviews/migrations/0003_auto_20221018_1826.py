# Generated by Django 2.2.16 on 2022-10-18 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20221018_1147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='group',
            new_name='role',
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
