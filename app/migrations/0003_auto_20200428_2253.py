# Generated by Django 2.2 on 2020-04-28 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_notification_admin_read_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='user_read_at',
            new_name='read_at',
        ),
    ]