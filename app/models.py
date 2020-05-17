import os
from datetime import datetime
from enum import Enum
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django_fsm import FSMField, transition
from django.contrib.auth.models import User, Permission
from PIL import Image
from django.urls import reverse

STAGES = ("Registry", "Reception", "Assembly", "Scanner", "Transcriber", "Quality Assuarance", "Validator")
STATES = ("Open", "In Progress", "Re Opened", "Done", "Closed",)
BATCH = ("Open", "In Progress", "Done", "Closed")






class Batch(models.Model):
    batch_no = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField( null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name='created_by')
    is_return_batch = models.BooleanField(null=False)
    state = FSMField(default=BATCH[0], protected=True)

    # transition methods
    @transition(field=state, source=['Open'], target='In Progress')
    def start(self, user=None):
        print(f'start user={user}')

        pass

    @transition(field=state, source=['In Progress'], target='Done')
    def done(self):
        pass

    @transition(field=state, source=['Done'], target='Closed')
    def close(self):
        pass

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

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    file_created_by = models.ForeignKey(User, null=True, blank=True,
                                        on_delete=models.DO_NOTHING,
                                        related_name='file_created_by')

    created_on = models.DateTimeField(auto_now_add=timezone.now)
    state = FSMField(default=STATES[0], protected=True)

    file_barcode = models.CharField(unique=True, max_length=255)
    flagged=models.BooleanField(default=False)

    assigned_to = models.ForeignKey(User, null=True, blank=True,
                                        on_delete=models.DO_NOTHING,
                                        related_name='file_assigned_to')
    file_path = models.CharField(null=True, max_length=100)
    stage = FSMField(default=STAGES[0], protected=True)

    def __str__(self):
        return self.file_reference

    def get_absolute_url(self):
        return reverse('view_docs_in_file', kwargs={'file_reference': self.pk})
    def file_closed(self):
        if self.state == STATES[4]:
            return True
        return False

    def assigned_to_me(self,user=None):
        if self.assigned_to == user:
            return True
        return False
    def assign_when_not_assigned(self,user=None):
        if self.assigned_to == user:
            return True
        elif self.assigned_to == None:
            self.assigned_to=user
            self.save()
            return True

        return False


    # transition methods
    @transition(field=state, source=['Open'], target='In Progress')
    def start(self,user=None):


        if self.assigned_to == None:
            self.assigned_to = user
            self.save()
        pass

    @transition(field=state, source=['In Progress'], target='Done',)
    def done(self):
        pass

    @transition(field=state, source=['Done'], target='Closed')
    def close(self):
        pass

    @transition(field=state, source=['Done'], target='Re Opened')
    def reopen(self):
        pass

    @transition(field=state, source=['Re Opened'], target='In Progress')
    def progress(self):
        pass

    @transition(field=stage, source=['Registry'], target='Reception',conditions=[file_closed],permission=['app.can_create_batch'])
    def dispatch_reception(self,user=None):

        #create log
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[0],
            modified_to_stage=STAGES[0],
            by=user
        )
        pass

    @transition(field=stage, source=['Reception'], target='Registry',conditions=[file_closed],permission=['app.can_receive_file'])
    def return_registry(self,user,rejection_comment=''):
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[1],
            modified_to_stage=STAGES[0],
            by=user
        )

        notification=Notification.objects.create(
            file=self,
            comment=rejection_comment
        )
        #user who created
        NotificationSentTo.objects.create(
            notification=notification,
            user=self.file_created_by
        )

        #all admins
        for user_obj in User.objects.filter(is_superuser=True):
            NotificationSentTo.objects.create(
                notification=notification,
                user=user_obj
            )


        self.assigned_to=self.file_created_by
        self.save()
        pass

    @transition(field=stage, source=['Reception'], target='Assembly',conditions=[file_closed],permission=['app.can_receive_file'])
    def dispatch_assembly(self,user=None):
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[1],
            modified_to_stage=STAGES[2],
            by=user
        )
        pass

    @transition(field=stage, source=['Assembly'], target='Reception',conditions=[file_closed],permission=['app.can_disassemble_file'])

    def return_assembly(self,user=None,rejection_comment=None):
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[2],
            modified_to_stage=STAGES[1],
            by=user
        )

        notification = Notification.objects.create(
            file=self,
            comment=rejection_comment
        )
        # user who did reception
        modified=Modification.objects.filter(modified_to_stage=STAGES[1]).last()
        NotificationSentTo.objects.create(
            notification=notification,
            user=modified.by
        )

        # all admins
        for user_obj in User.objects.filter(is_superuser=True):
            NotificationSentTo.objects.create(
                notification=notification,
                user=user_obj
            )

        self.assigned_to = modified.by
        self.save()
        pass

    @transition(field=stage, source=['Assembly'], target='Scanner',conditions=[file_closed],permission=['app.can_disassemble_file'])
    def dispatch_scanner(self,user):
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[2],
            modified_to_stage=STAGES[3],
            by=user
        )
        pass

    @transition(field=stage, source=['Scanner'], target='Transcriber',conditions=[file_closed],permission=['app.can_scan_file'])
    def dispatch_transcriber(self,user=None):
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[3],
            modified_to_stage=STAGES[4],
            by=user
        )
        pass

    @transition(field=stage, source=['Transcriber'], target='Quality Assurance',conditions=[file_closed],permission=['app.can_transcribe_file'])
    def dispatch_qa(self,user=None):
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[4],
            modified_to_stage=STAGES[5],
            by=user
        )
        pass

    @transition(field=stage, source=['Quality Assurance'], target='Validator',conditions=[file_closed],permission=['app.can_qa_file'])
    def dispatch_validator(self,user=None):
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[5],
            modified_to_stage=STAGES[6],
            by=user
        )
        pass

    @transition(field=stage, source=['Validator'], target='Reception',conditions=[file_closed],permission=['app.can_validate_file'])
    def finalize_to_reception(self):
        pass


class DocumentFileDetail(models.Model):
    file_reference = models.ForeignKey(DocumentFile, db_column="file_reference", on_delete=models.CASCADE, null=True)
    document_barcode = models.CharField(unique=True,max_length=255)

    document_name = models.CharField(max_length=255, blank=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True)

    document_content = JSONField(null=True)
    document_file_path = models.CharField(null=True, max_length=100)
    doc_created_by = models.ForeignKey(User, null=True, blank=True,
                                       on_delete=models.DO_NOTHING,
                                       related_name='doc_created_by')
    created_on = models.DateTimeField(auto_now_add=timezone.now)




    assigned_to = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.DO_NOTHING,
                                    related_name='doc_assigned_to')


    state = FSMField(default=STATES[0], protected=True)



    # transition methods
    @transition(field=state, source=['Open'], target='In Progress')
    def start(self):
        pass

    @transition(field=state, source=['In Progress'], target='Done')
    def done(self):
        pass

    @transition(field=state, source=['Done'], target='Closed')
    def close(self):
        pass

    @transition(field=state, source=['Done'], target='Re Opened')
    def reopen(self):
        pass

    @transition(field=state, source=['Re Opened'], target='In Progress')
    def progress(self):
        pass

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



    file = models.ForeignKey(DocumentFile,on_delete=models.CASCADE)
    modified_from_stage =FSMField(null=False, protected=True)
    modified_to_stage = FSMField(null=True, protected=True)
    by = models.ForeignKey(User, on_delete=models.CASCADE)



class Notification(models.Model):

    """all notifications"""

    file = models.ForeignKey(DocumentFile,on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
class NotificationSentTo(models.Model):

    notification=models.ForeignKey(Notification,on_delete=models.CASCADE,null=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    read_at = models.DateTimeField(null=True)




