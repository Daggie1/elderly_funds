# Generated by Django 2.2 on 2020-03-26 06:35

import app.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20200326_0508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfiledetail',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='documentstate',
            name='document_quality_control',
            field=models.CharField(choices=[('UNASSESSED', 'Unassessed'), ('REJECTED', 'Rejected'), ('APPROVED', 'Approved')], default=app.models.StateOptions('Unassessed'), max_length=255),
        ),
        migrations.AlterField(
            model_name='documentstate',
            name='document_validation_status',
            field=models.CharField(choices=[('UNASSESSED', 'Unassessed'), ('REJECTED', 'Rejected'), ('APPROVED', 'Approved')], default=app.models.StateOptions('Unassessed'), max_length=255),
        ),
    ]
