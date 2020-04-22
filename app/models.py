import os
from datetime import datetime
from enum import Enum
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.contrib.auth.models import User, Permission
from PIL import Image
from django.urls import reverse


# Create your models here.
class StateOptions(Enum):
    REGISTRY = 'Registry'  # pk = 300
    AWAITING_RECEIVE = 'Awaiting Receive'  # pk = 301
    AWAITING_DISASSEMBLER = 'Awaiting Disassembler'  # pk = 302
    AWAITING_SCANNING = 'Awaiting Scanning'  # pk = 303
    AWAITING_REASSEMBLER = 'Awaiting Reassembler'  # pk = 304
    AWAITING_TRANSCRIPTION = 'Awaiting Transcription'  # pk = 305
    AWAITING_QA = 'Awaiting QA'  # pk = 306
    AWAITING_VALIDATION = 'Awaiting Validation'  # pk = 307
    FULL_VALIDATED = 'Fully validated'  # pk = 308
    REGISTRY_REJECTED = 'Rejected to Registry'  # pk = 400
    RECEIVE_REJECTED = 'Returned to Receiver'  # pk = 401
    DISASSEMBLER_REJECTED = 'Returned to Scanner'  # pk = 402
    SCANNER_REJECTED = 'Rejected to transcriber'  # pk = 403
    REASSEMBLER_REJECTED = 'Rejected to transcriber'  # pk = 404
    TRANSCRIPTION_REJECTED = 'Rejected at Transcription'  # pk = 405
    QA_REJECTED = 'Rejected at QA'  # pk = 406
    VALIDATION_REJECTED = 'Rejected at Validation'  # pk = 407
    ADMIN_REJECTED = 'Rejected by Admin'  # pk = 408

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
#TODO -make barcodes unique

class DocumentState(models.Model):
    state_code = models.CharField(max_length=255, primary_key=True)
    state_name = models.CharField(max_length=255)

    permission = models.ForeignKey(Permission, on_delete=models.DO_NOTHING)

    state_parameter = models.CharField(max_length=255)

    state = models.CharField(max_length=255,
                             choices=StateOptions.choices(),
                             default=StateOptions.REGISTRY
                             )

    def __str__(self):
        return self.state_name


class Batch(models.Model):
    batch_no = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField( null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name='created_by')


    state = models.ForeignKey(DocumentState, null=True, on_delete=models.DO_NOTHING)



    def __str__(self):
        return self.batch_no


class DocumentFileType(models.Model):
    file_type = models.CharField(max_length=100, null=False, primary_key=True)
    file_description = models.CharField(max_length=255)

    def __str__(self):
        return self.file_type


class DocumentType(models.Model):
    document_name = models.CharField(max_length=255, primary_key=True)
    document_field_specs = JSONField()
    document_description = models.CharField(max_length=255)

    def __str__(self):
        return self.document_name


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


    file_barcode = models.CharField(null=True, max_length=255)
    state = models.ForeignKey(DocumentState, null=True, on_delete=models.DO_NOTHING)

    file_path = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.file_reference

    def get_absolute_url(self):
        return reverse('view_docs_in_file', kwargs={'file_reference': self.pk})


class DocumentFileDetail(models.Model):
    file_reference = models.ForeignKey(DocumentFile, db_column="file_reference", on_delete=models.CASCADE, null=True)
    document_barcode = models.CharField(max_length=255)

    document_name = models.CharField(max_length=255, blank=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True)

    document_content = JSONField(null=True)
    document_file_path = models.CharField(null=True, max_length=100)
    doc_created_by = models.ForeignKey(User, null=True, blank=True,
                                       on_delete=models.DO_NOTHING,
                                       related_name='doc_created_by')
    created_on = models.DateTimeField(auto_now_add=timezone.now)

    state = models.ForeignKey(DocumentState, null=True, on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.document_barcode







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
    batch = instance.file_reference.batch

    path = 'media/%d/{}/{}/{}{}'.format(batch, folder, name, ext)
    return datetime.now().strftime(path)


class Filer(models.Model):
    """
    create an initial folder
    create a new folder if it has more than 2000 files inside it
    """
    filepond = models.FileField(upload_to=document_directory_path)
    file_reference = models.ForeignKey(DocumentFile, related_name='documents', on_delete=models.CASCADE)
    document_reference = models.CharField(null=True, max_length=40)

    def filename(self):
        return os.path.basename(self.filepond.name)





class Modification(models.Model):

    """ This tables all the modifications of either batch,file or document-will be used to track the action workflow"""


    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # either batch, file, doc
    object_pk = models.CharField(max_length=255) # the pk of the object being modified
    modification_started_at = models.DateTimeField(auto_now_add=timezone.now) # time when select to start modifying
    modification_ended_at = models.DateTimeField(null=True)  # time when you submit object to next state after modification
    modified_from_state = models.ForeignKey(DocumentState,related_name='modified_from_state', on_delete=models.CASCADE )
    modified_to_state = models.ForeignKey(DocumentState, related_name='modified_to_state', on_delete=models.CASCADE, null=True)
    by = models.ForeignKey(User, on_delete=models.CASCADE)



class Notification(models.Model):


    """all notifications"""


    to = models.ForeignKey(User, on_delete=models.CASCADE)
    user_read_at = models.DateTimeField(null=True) # if null means not read
    admin_read_at = models.DateTimeField(null=True)
    modification=models.ForeignKey(Modification,on_delete=models.CASCADE)
    comment = models.TextField(null=True)

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


# class DocumentWorkFlow(models.Model):
#     current_node_id = models.CharField(max_length=50, primary_key=True)
#     current_state_code = models.CharField(max_length=10)
#     current_state_name = models.CharField(max_length=40)
#     state_transition_parameter = models.CharField(max_length=5)
#     document_validation_status = models.CharField(max_length=40)
#     document_quality_control = models.CharField(max_length=40)
#     transition_code = models.CharField(max_length=40)
#     transition_name = models.CharField(max_length=40)
#     next_node_id = models.CharField(max_length=40)
#     next_state_code = models.CharField(max_length=40)
#     next_state = models.CharField(max_length=40)
#     document = models.ForeignKey(DocumentFileDetail, null=True, on_delete=models.CASCADE)
#     document_file = models.ForeignKey(DocumentFile, null=True, on_delete=models.CASCADE)