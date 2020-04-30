# Generated by Django 2.2 on 2020-04-28 14:22

import app.models
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_no', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('file_reference', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('document', models.FileField(upload_to='documents')),
                ('file_status', models.CharField(max_length=100, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('file_barcode', models.CharField(max_length=255, null=True)),
                ('file_path', models.CharField(max_length=100, null=True)),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Batch')),
                ('file_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentFileType',
            fields=[
                ('file_type', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('file_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentState',
            fields=[
                ('state_code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('state_name', models.CharField(max_length=255)),
                ('state_parameter', models.CharField(max_length=255)),
                ('state', models.CharField(choices=[('REGISTRY', 'Registry'), ('AWAITING_RECEIVE', 'Awaiting Receive'), ('AWAITING_DISASSEMBLER', 'Awaiting Disassembler'), ('AWAITING_SCANNING', 'Awaiting Scanning'), ('AWAITING_REASSEMBLER', 'Awaiting Reassembler'), ('AWAITING_TRANSCRIPTION', 'Awaiting Transcription'), ('AWAITING_QA', 'Awaiting QA'), ('AWAITING_VALIDATION', 'Awaiting Validation'), ('FULL_VALIDATED', 'Fully validated'), ('REGISTRY_REJECTED', 'Rejected to Registry'), ('RECEIVE_REJECTED', 'Returned to Receiver'), ('DISASSEMBLER_REJECTED', 'Returned to Scanner'), ('SCANNER_REJECTED', 'Rejected to transcriber'), ('TRANSCRIPTION_REJECTED', 'Rejected at Transcription'), ('QA_REJECTED', 'Rejected at QA'), ('VALIDATION_REJECTED', 'Rejected at Validation'), ('ADMIN_REJECTED', 'Rejected by Admin')], default=app.models.StateOptions('Registry'), max_length=255)),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='auth.Permission')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('document_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('document_field_specs', django.contrib.postgres.fields.jsonb.JSONField()),
                ('document_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Modification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_pk', models.CharField(max_length=255)),
                ('modification_started_at', models.DateTimeField(auto_now_add=True)),
                ('modification_ended_at', models.DateTimeField(null=True)),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('modified_from_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modified_from_state', to='app.DocumentState')),
                ('modified_to_state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_to_state', to='app.DocumentState')),
                ('object_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_no', models.CharField(max_length=25, null=True)),
                ('phone', models.CharField(max_length=25, null=True)),
                ('full_name', models.CharField(max_length=25, null=True)),
                ('first_login', models.BooleanField(default=True)),
                ('image', models.ImageField(default='default.jpg', null=True, upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_read_at', models.DateTimeField(null=True)),
                ('admin_read_at', models.DateTimeField(null=True)),
                ('comment', models.TextField(null=True)),
                ('modification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Modification')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Filer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepond', models.FileField(upload_to=app.models.document_directory_path)),
                ('document_reference', models.CharField(max_length=40, null=True)),
                ('file_reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='app.DocumentFile')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentFileDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_barcode', models.CharField(max_length=255)),
                ('document_name', models.CharField(blank=True, max_length=255)),
                ('document_content', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('document_file_path', models.CharField(max_length=100, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('doc_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_created_by', to=settings.AUTH_USER_MODEL)),
                ('document_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.DocumentType')),
                ('file_reference', models.ForeignKey(db_column='file_reference', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.DocumentFile')),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.DocumentState')),
            ],
        ),
        migrations.AddField(
            model_name='documentfile',
            name='file_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.DocumentFileType'),
        ),
        migrations.AddField(
            model_name='documentfile',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.DocumentState'),
        ),
        migrations.AddField(
            model_name='batch',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.DocumentState'),
        ),
    ]
