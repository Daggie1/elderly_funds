# Generated by Django 2.2 on 2020-05-23 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfiledetail',
            name='passed_qa',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='documentfiledetail',
            name='passed_validated',
            field=models.BooleanField(default=False),
        ),
    ]
