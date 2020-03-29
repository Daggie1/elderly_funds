from enum import Enum

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


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
    created_on = models.DateTimeField(auto_now_add=timezone.now)
    assessed_by = models.CharField(max_length=100, null=True)
    assessed_on = models.DateTimeField(auto_now_add=timezone.now, null=True)
    validated_by = models.CharField(max_length=100, null=True)
    file_barcode = models.CharField(null=True, max_length=100)


class StateOptions(Enum):

        UNASSESSED = 'Unassessed'
        REJECTED = 'Rejected'
        APPROVED = 'Approved'

        @classmethod
        def choices(cls):

            return tuple((i.name, i.value) for i in cls)

class DocumentState(models.Model):
    state_code = models.CharField(max_length=255)
    state_name = models.CharField(max_length=255)
    state_parameter = models.CharField(max_length=255)

    document_validation_status = models.CharField(max_length=255,
                                                  choices=StateOptions.choices(),
                                                  default=StateOptions.UNASSESSED
                                                  )
    document_quality_control = models.CharField(max_length=255,
                                                choices=StateOptions.choices(),
                                                default=StateOptions.UNASSESSED
                                                )


class DocumentFileDetail(models.Model):
    file_reference = models.ForeignKey(DocumentFile, on_delete=models.CASCADE)
    document_barcode = models.CharField(max_length=255)
    document_name = models.ForeignKey(DocumentType, db_column="file_reference", on_delete=models.CASCADE)
    document_content = JSONField(null=True)
    document_file_path = models.FileField(upload_to='documents')
    created_on = models.DateTimeField(default=timezone.now)
    captured_by = models.CharField(max_length=255, null=True)
    assessed_by = models.CharField(max_length=255, null=True)
    validated_by = models.CharField(max_length=255, null=True)
    state = models.ForeignKey(DocumentState, db_column='state_code', on_delete=models.CASCADE)


#
#
#

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

class DocumentWorkFlow(models.Model):
    current_node_id = models.CharField(max_length=50, primary_key=True)
    current_state_code = models.CharField(max_length=10)
    current_state_name = models.CharField(max_length=40)
    state_transition_parameter = models.CharField(max_length=5)
    document_validation_status = models.CharField(max_length=40)
    document_quality_control = models.CharField(max_length=40)
    transition_code = models.CharField(max_length=40)
    transition_name = models.CharField(max_length=40)
    next_node_id = models.CharField(max_length=40)
    next_state_code = models.CharField(max_length=40)
    next_state = models.CharField(max_length=40)
    document = models.ForeignKey(DocumentFileDetail, null=True, on_delete=models.CASCADE)
    document_file = models.ForeignKey(DocumentFile, null=True, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_no = models.CharField(null=True, max_length=25)
    phone = models.CharField(null=True, max_length=25)
    full_name = models.CharField(null=True, max_length=25)
    first_login = models.BooleanField(default=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
