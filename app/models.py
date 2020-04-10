import os
from datetime import datetime
from enum import Enum

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.contrib.auth.models import User, Group
from PIL import Image


# Create your models here.
class StateOptions(Enum):
    REGISTRY = 'Registry'  # 300
    AWAITING_RECEIVE = 'Awaiting Receive'  # 301
    RECEIVE_REJECTED = 'Rejected at Receive'  # 302
    AWAITING_SCANNING = 'Awaiting Scanning'  # 303
    AWAITING_TRANSCRIPTION = 'Awaiting Transcription'  # 304
    TRANSCRIPTION_REJECTED = 'Rejected at transcription'  # 305
    AWAITING_QA = 'Awaiting QA'  # 306
    QA_REJECTED = 'rejected at QA'  # 307
    AWAITING_VALIDATION = 'Awaiting Validation'  # 308
    VALIDATION_REJECTED = 'Rejected at Validation'  # 309
    FULL_VALIDATED = 'Fully validated'  # 310

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class DocumentState(models.Model):
    state_code = models.CharField(max_length=255, primary_key=True)
    state_name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    state_parameter = models.CharField(max_length=255)

    state = models.CharField(max_length=255,
                             choices=StateOptions.choices(),
                             default=StateOptions.REGISTRY
                             )


class Batch(models.Model):
    batch_no = models.CharField(max_length=255, null=False, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=timezone.now)
    released_on = models.DateTimeField(null=True)
    received_on = models.DateTimeField(null=True)
    returned_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name='created_by')
    received_by = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.DO_NOTHING,
                                    related_name='received_by')
    receive_state = models.ForeignKey(DocumentState, null=True, blank=True,
                                      on_delete=models.DO_NOTHING,
                                      related_name='received_state')
    return_state = models.ForeignKey(DocumentState, null=True, blank=True,
                                     on_delete=models.DO_NOTHING,
                                     related_name='return_state')
    state = models.ForeignKey(DocumentState, null=True, on_delete=models.DO_NOTHING)
    rejection_by_receiver_dec = models.TextField(null=True, blank=True)


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
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    file_created_by = models.ForeignKey(User, null=True, blank=True,
                                        on_delete=models.DO_NOTHING,
                                        related_name='file_created_by')
    created_on = models.DateTimeField(auto_now_add=timezone.now)
    file_scanned_by = models.ForeignKey(User, null=True, blank=True,
                                        on_delete=models.DO_NOTHING,
                                        related_name='file_scanned_by')
    scanned_on = models.DateTimeField(null=True)
    file_transcribed_by = models.ForeignKey(User, null=True, blank=True,
                                            on_delete=models.DO_NOTHING,
                                            related_name='file_transcribed_by')
    transcribed_on = models.DateTimeField(null=True)
    file_qa_by = models.ForeignKey(User, null=True, blank=True,
                                   on_delete=models.DO_NOTHING,
                                   related_name='file_qa_by')
    qa_on = models.DateTimeField(null=True)
    file_validated_by = models.ForeignKey(User, null=True, blank=True,
                                          on_delete=models.DO_NOTHING,
                                          related_name='file_validated_by')
    validated_on = models.DateTimeField(null=True)
    file_barcode = models.CharField(null=True, max_length=255)
    rejection_by_scanner_dec = models.TextField(null=True, blank=True)
    rejection_by_transcriber_dec = models.TextField(null=True, blank=True)
    rejection_by_aq_dec = models.TextField(null=True, blank=True)
    rejection_by_validation_dec = models.TextField(null=True, blank=True)
    file_path = models.CharField(null=True, max_length=100)


class DocumentFileDetail(models.Model):
    file_reference = models.ForeignKey(DocumentFile, db_column="file_reference", on_delete=models.CASCADE, null=True)
    document_barcode = models.CharField(max_length=255)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True)
    document_content = JSONField(null=True)
    filepond = models.FileField(upload_to='documents')
    doc_created_by = models.ForeignKey(User, null=True, blank=True,
                                       on_delete=models.DO_NOTHING,
                                       related_name='doc_created_by')
    created_on = models.DateTimeField(auto_now_add=timezone.now)
    doc_scanned_by = models.ForeignKey(User, null=True, blank=True,
                                       on_delete=models.DO_NOTHING,
                                       related_name='doc_scanned_by')
    scanned_on = models.DateTimeField(null=True)
    doc_transcribed_by = models.ForeignKey(User, null=True, blank=True,
                                           on_delete=models.DO_NOTHING,
                                           related_name='doc_transcribed_by')
    transcribed_on = models.DateTimeField(null=True)
    doc_qa_by = models.ForeignKey(User, null=True, blank=True,
                                  on_delete=models.DO_NOTHING,
                                  related_name='doc_qa_by')
    qa_on = models.DateTimeField(null=True)
    doc_validated_by = models.ForeignKey(User, null=True, blank=True,
                                         on_delete=models.DO_NOTHING,
                                         related_name='doc_validated_by')
    validated_on = models.DateTimeField(null=True)
    rejection_by_scanner_dec = models.TextField(null=True, blank=True)
    rejection_by_transcriber_dec = models.TextField(null=True, blank=True)
    rejection_by_aq_dec = models.TextField(null=True, blank=True)
    rejection_by_validation_dec = models.TextField(null=True, blank=True)
    state = models.ForeignKey(DocumentState, db_column='state_code', on_delete=models.CASCADE, null=True)


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
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


def document_directory_path(instance, filename):
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    folder = instance.file_reference.file_reference
    file_type = ""

    file_type = "others"
    path = 'media/uploads/%Y/%d/{}/{}/{}{}'.format(folder,file_type, name, ext)
    print(path)
    return datetime.now().strftime(path)


class Filer(models.Model):
    """
    create an initial folder
    create a new folder if it has more than 2000 files inside it
    """
    filepond = models.FileField(upload_to=document_directory_path)
    file_reference = models.ForeignKey(DocumentFile,related_name='documents', on_delete=models.CASCADE)
    document_reference = models.CharField(null=True, max_length=40)

    def filename(self):
        return os.path.basename(self.filepond.name)
