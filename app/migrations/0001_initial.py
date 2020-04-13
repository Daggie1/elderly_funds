# Generated by Django 2.2 on 2020-04-13 09:11

import app.models
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_no', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('released_on', models.DateTimeField(null=True)),
                ('received_on', models.DateTimeField(null=True)),
                ('returned_on', models.DateTimeField(null=True)),
                ('rejection_by_receiver_dec', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('received_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='received_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('file_reference', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('document', models.FileField(upload_to='documents')),
                ('file_status', models.CharField(max_length=100, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('scanned_on', models.DateTimeField(null=True)),
                ('transcribed_on', models.DateTimeField(null=True)),
                ('qa_on', models.DateTimeField(null=True)),
                ('validated_on', models.DateTimeField(null=True)),
                ('file_barcode', models.CharField(max_length=255, null=True)),
                ('rejection_by_scanner_dec', models.TextField(blank=True, null=True)),
                ('rejection_by_transcriber_dec', models.TextField(blank=True, null=True)),
                ('rejection_by_aq_dec', models.TextField(blank=True, null=True)),
                ('rejection_by_validation_dec', models.TextField(blank=True, null=True)),
                ('file_path', models.CharField(max_length=100, null=True)),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Batch')),
                ('file_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_created_by', to=settings.AUTH_USER_MODEL)),
                ('file_qa_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_qa_by', to=settings.AUTH_USER_MODEL)),
                ('file_scanned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_scanned_by', to=settings.AUTH_USER_MODEL)),
                ('file_transcribed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_transcribed_by', to=settings.AUTH_USER_MODEL)),
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
                ('scanned_on', models.DateTimeField(null=True)),
                ('transcribed_on', models.DateTimeField(null=True)),
                ('qa_on', models.DateTimeField(null=True)),
                ('validated_on', models.DateTimeField(null=True)),
                ('rejection_by_scanner_dec', models.TextField(blank=True, null=True)),
                ('rejection_by_transcriber_dec', models.TextField(blank=True, null=True)),
                ('rejection_by_aq_dec', models.TextField(blank=True, null=True)),
                ('rejection_by_validation_dec', models.TextField(blank=True, null=True)),
                ('doc_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_created_by', to=settings.AUTH_USER_MODEL)),
                ('doc_qa_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_qa_by', to=settings.AUTH_USER_MODEL)),
                ('doc_scanned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_scanned_by', to=settings.AUTH_USER_MODEL)),
                ('doc_transcribed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_transcribed_by', to=settings.AUTH_USER_MODEL)),
                ('doc_validated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='doc_validated_by', to=settings.AUTH_USER_MODEL)),
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
            name='DocumentType',
            fields=[
                ('document_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('document_field_specs', django.contrib.postgres.fields.jsonb.JSONField()),
                ('document_description', models.CharField(max_length=255)),
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
            name='Filer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepond', models.FileField(upload_to=app.models.document_directory_path)),
                ('document_reference', models.CharField(max_length=40, null=True)),
                ('file_reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='app.DocumentFile')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentWorkFlow',
            fields=[
                ('current_node_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('current_state_code', models.CharField(max_length=10)),
                ('current_state_name', models.CharField(max_length=40)),
                ('state_transition_parameter', models.CharField(max_length=5)),
                ('document_validation_status', models.CharField(max_length=40)),
                ('document_quality_control', models.CharField(max_length=40)),
                ('transition_code', models.CharField(max_length=40)),
                ('transition_name', models.CharField(max_length=40)),
                ('next_node_id', models.CharField(max_length=40)),
                ('next_state_code', models.CharField(max_length=40)),
                ('next_state', models.CharField(max_length=40)),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.DocumentFileDetail')),
                ('document_file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.DocumentFile')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentState',
            fields=[
                ('state_code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('state_name', models.CharField(max_length=255)),
                ('state_parameter', models.CharField(max_length=255)),
                ('state', models.CharField(choices=[('REGISTRY', 'Registry'), ('AWAITING_RECEIVE', 'Awaiting Receive'), ('RECEIVE_REJECTED', 'Rejected at Receive'), ('AWAITING_SCANNING', 'Awaiting Scanning'), ('AWAITING_TRANSCRIPTION', 'Awaiting Transcription'), ('TRANSCRIPTION_REJECTED', 'Rejected at transcription'), ('AWAITING_QA', 'Awaiting QA'), ('QA_REJECTED', 'Rejected at QA'), ('AWAITING_VALIDATION', 'Awaiting Validation'), ('VALIDATION_REJECTED', 'Rejected at Validation'), ('FULL_VALIDATED', 'Fully validated')], default=app.models.StateOptions('Registry'), max_length=255)),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='auth.Permission')),
            ],
        ),
        migrations.AddField(
            model_name='documentfiledetail',
            name='document_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.DocumentType'),
        ),
        migrations.AddField(
            model_name='documentfiledetail',
            name='file_reference',
            field=models.ForeignKey(db_column='file_reference', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.DocumentFile'),
        ),
        migrations.AddField(
            model_name='documentfiledetail',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.DocumentState'),
        ),
        migrations.AddField(
            model_name='documentfile',
            name='file_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.DocumentFileType'),
        ),
        migrations.AddField(
            model_name='documentfile',
            name='file_validated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_validated_by', to=settings.AUTH_USER_MODEL),
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
