# Generated by Django 2.2 on 2020-03-19 02:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentfile',
            name='id',
        ),
        migrations.AddField(
            model_name='documentfile',
            name='file_reference',
            field=models.CharField(default='rno', max_length=100, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='assessed_by',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='assessed_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='captured_by',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='file_status',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='validated_by',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='documentfiledetail',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 19, 2, 8, 46, 29726, tzinfo=utc)),
        ),
    ]
