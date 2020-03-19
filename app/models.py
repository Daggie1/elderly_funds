from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone


# Create your models here.


class DocumentFileType(models.Model):
    file_type = models.CharField(max_length=100, null=False, primary_key=True)
    file_description = models.CharField(max_length=255)


class DocumentType(models.Model):
    document_name = models.CharField(max_length=255, primary_key=True)
    document_field_specs = JSONField()
    document_description = models.CharField(max_length=255)


#
class DocumentFile(models.Model):
    file_reference = models.CharField(primary_key=True, max_length=100)
    file_type = models.ForeignKey(DocumentFileType, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents')
    file_status = models.CharField(max_length=100, null=True)
    captured_by = models.CharField(max_length=100, null=True)
    created_on = models.DateTimeField(auto_now_add=timezone.now())
    assessed_by = models.CharField(max_length=100, null=True)
    assessed_on = models.DateTimeField(auto_now_add=timezone.now(), null=True)
    validated_by = models.CharField(max_length=100, null=True)
    file_barcode = models.CharField(null=True, max_length=100)

class DocumentFileDetail(models.Model):
    file_detail_id = models.AutoField(primary_key=True)
    file_reference = models.ForeignKey(DocumentFileType, on_delete=models.CASCADE)
    document_barcode = models.CharField(max_length=255)
    document_name =models.ForeignKey(DocumentFile, on_delete=models.CASCADE)
    document_content = JSONField()
    document_file_path = models.CharField(max_length=255)
    created_on = models.DateTimeField(default=timezone.now())
    captured_by = models.CharField(max_length=255)
    assessed_by = models.CharField(max_length=255)
    validated_by = models.CharField(max_length=255)
#
#
#
# class DocumentState(models.Model):
#     state_code = models.CharField()
#     state_name = models.CharField()
#     state_paremeter = models.CharField()
#     document_validation_status = models.CharField()
#     document_quality_control = models.CharField()
#
# class DocumentStateTransition(models.Model):
#     transition_code = models.CharField()
#     transition_name = models.CharField()
#     transition_paremeter = models.CharField()
#     current_state_code = models.CharField()
#     current_state = models.CharField()
#     next_state_code = models.CharField()
#     next_state = models.CharField()
#     pre_condition = models.CharField()
#
# class DocumentWorkFlow(models.Model):
#     current_node_id = models.CharField()
#     current_state_code = models.CharField()
#     current_state_name = models.CharField()
#     state_transition_parameter = models.CharField()
#     document_validation_status = models.CharField()
#     document_quality_control = models.CharField()
#     transition_code = models.CharField()
#     transition_name = models.CharField()
#     next_node_id = models.CharField()
#     next_state_code = models.CharField()
#     next_state = models.CharField()
