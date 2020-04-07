# Generated by Django 2.2 on 2020-04-02 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200402_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfile',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.DocumentState'),
        ),
        migrations.AlterField(
            model_name='documentfiledetail',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.DocumentState'),
        ),
    ]
