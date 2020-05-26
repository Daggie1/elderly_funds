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
STATES = ("Opened", "Done", "Closed",)
BATCH = ("Opened","Done","Closed")


class Batch(models.Model):
    batch_no = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name='created_by')
    is_return_batch = models.BooleanField(null=False)
    state = FSMField(default=BATCH[0], protected=True)

    # transition methods
    @transition(field=state, source=[BATCH[2]], target=BATCH[0])
    def open(self, user=None):

        """opening a closed file"""

        pass

    @transition(field=state, source=[BATCH[0]], target=BATCH[1])
    def done(self):

        """"staging a batch once done adding files and docs
         -moves state of files in batch to DONE
        -moves batch state to DONE
         """

        files = DocumentFile.objects.filter(batch=self)
        for file in files:
            file.done()
            file.save()

    @transition(field=state, source=[BATCH[1]], target=BATCH[0])
    def continue_editing(self):
        """"unstaging a staged batch to add/edit/delete some files and docs
                 -moves state of files in batch to Open
                -moves batch state to Open
                 """
        files = DocumentFile.objects.filter(batch=self)
        for file in files:
            file.continue_editing()
            file.save()
        pass

    @transition(field=state, source=[BATCH[1]], target=BATCH[2])
    def close(self, user=None, comment=''):
        """"closes a batch
                 -moves state of files in batch to CLOSE
                -moves batch state to CLOSE
                -moves stage files in batch to RECEPTION

                this action is permanent
                 """
        files = DocumentFile.objects.filter(batch=self)
        if not self.is_return_batch:
            for file in files:
                file.close()
                file.dispatch_reception(user=user)
                file.save()
        else:
            for file in files:
                file.close()
                file.return_registry(user=user, rejection_comment=comment)
                file.save()

    def get_transition_options(self):
        transition = list(self.get_available_state_transitions())
        # "Opened", "Done", "Closed"
        # 'Open', 'Done', 'Continue_Editing', 'Close'
        if transition[0].target == "Opened":
            return "Open"
        elif transition[0].target == "Done":
            return "Done"
        else:
            return "Close"

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
    flagged = models.BooleanField(default=False)

    assigned_to = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.DO_NOTHING,
                                    related_name='file_assigned_to')
    lock = models.BooleanField(default=False)
    file_path = models.CharField(null=True, max_length=100)
    stage = FSMField(default=STAGES[0], protected=True)

    def __str__(self):
        return self.file_reference

    def get_absolute_url(self):
        return reverse('view_docs_in_file', kwargs={'file_reference': self.pk})

    def file_closed(self):
        if self.state == STATES[3]:
            return True
        return False

    def assigned_to_me(self, user=None):
        if self.assigned_to == user:
            return True
        return False

    def assign_when_not_assigned(self, user=None):
        if self.assigned_to == user:
            return True
        elif self.assigned_to == None:
            self.assigned_to = user
            self.save()
            return True

        return False

    # transition methods
    @transition(field=state, source=[STATES[2]], target=STATES[0])
    def open(self, user=None):
        """"changes  file state to OPEN
       if unassigned: assigns to current user
                         """

        if self.assigned_to == None:
            self.assigned_to = user
            self.save()
        pass

    @transition(field=state, source=[STATES[0]], target=STATES[1], )
    def done(self):
        """"changes  file state to DONE

                                 """
        pass

    @transition(field=state, source=[STATES[1]], target=STATES[0], )
    def continue_editing(self):
        """"changes  file state to OPEN

                                 """
        pass

    @transition(field=state, source=STATES[1], target=STATES[2])
    def close(self):
        """"changes  file state to OPEN
               -changes assigned to null
                                 """
        self.assigned_to = None
        self.save()
        pass

    @transition(field=stage, source=STAGES[0], target=STAGES[1])
    def dispatch_reception(self, user=None):
        """"changes  file stage to RECEPTION

            -records this action in Modification Table
                                 """
        # create log
        print(f'file being moved={self}')
        log=Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[0],
            modified_to_stage=STAGES[1],
            by=user
        )
        print(f'log created={log}')
        self.flagged=False
        self.save()

    @transition(field=stage, source=[STAGES[1]], target=STAGES[0], permission=['app.can_receive_file'])
    def return_registry(self,user,rejection_comment=''):


        """"flags a  file stage to REGISTRY

                    -records this action in Modification Table
                    -notify user who created
                    -notify all admins
                               """
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[1],
            modified_to_stage=STAGES[0],
            by=user
        )

        notification = Notification.objects.create(
            file=self,
            comment=rejection_comment
        )
        # user who created
        NotificationSentTo.objects.create(
            notification=notification,
            user=self.file_created_by
        )

        # all admins
        for user_obj in User.objects.filter(is_superuser=True):
            NotificationSentTo.objects.create(
                notification=notification,
                user=user_obj
            )

        self.assigned_to = self.file_created_by
        self.flagged = True
        self.save()

    @transition(field=stage, source=[STAGES[1]], target=STAGES[2],
                permission=['app.can_receive_file'])
    def dispatch_assembly(self, user=None):

        """"changes  file stage to ASSEMBLY

                    -records this action in Modification Table
                                         """
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[1],
            modified_to_stage=STAGES[2],
            by=user
        )
        self.flagged = False
        self.save()

#TODO remember conditions=[file_closed] hahah.....

    @transition(field=stage, source=[STAGES[2]], target=STAGES[1],
                permission=['app.can_disassemble_file'])
    def return_reception(self, user=None, rejection_comment=None):

        """"flags a  file stage to RECEPTION

                            -records this action in Modification Table
                            -notify user who edited at reception
                            -notify all admins
                                                 """
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
        modified = Modification.objects.filter(modified_to_stage=STAGES[1]).last()
        if modified:
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
        if modified:
            self.assigned_to = modified.by
        else:
            self.assigned_to = None
        self.flagged = True
        self.save()
        pass

    @transition(field=stage, source=[STAGES[2]], target=STAGES[3],
                permission=['app.can_disassemble_file'])
    def dispatch_scanner(self, user):
        """"changes  file stage to SCANNER

                    -records this action in Modification Table
                                         """
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[2],
            modified_to_stage=STAGES[3],
            by=user
        )
        self.flagged = False
        self.save()
    def return_reception(self, user=None, rejection_comment=None):

        """"flags a  file stage to RECEPTION

                            -records this action in Modification Table
                            -notify user who edited at reception
                            -notify all admins
                                                 """
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
        modified = Modification.objects.filter(modified_to_stage=STAGES[1]).last()
        if modified:
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
        if modified:
            self.assigned_to = modified.by
        else:
            self.assigned_to = None
        self.flagged = True
        self.save()
        pass
    @transition(field=stage, source=[STAGES[3]], target=STAGES[4],
                permission=['app.can_scan_file'])
    def dispatch_transcriber(self, user=None):

        """"changes  file stage to TRANSCRIBER

                    -records this action in Modification Table
                                         """
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[3],
            modified_to_stage=STAGES[4],
            by=user
        )
        self.flagged = False
        self.save()

    @transition(field=stage, source=[STAGES[4]], target=STAGES[3],
                permission=['app.can_transcribe_file'])
    def return_scanner(self, user=None, rejection_comment=None):

        """"flags a  file stage to SCANNER

                            -records this action in Modification Table
                            -notify user who edited at reception
                            -notify all admins
                                                 """
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[4],
            modified_to_stage=STAGES[3],
            by=user
        )

        notification = Notification.objects.create(
            file=self,
            comment=rejection_comment
        )
        # user who did reception
        modified = Modification.objects.filter(modified_to_stage=STAGES[3]).last()
        if modified:
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
        if modified:
            self.assigned_to = modified.by
        else:
            self.assigned_to = None
        self.flagged = True
        self.save()

    @transition(field=stage, source=[STAGES[4]], target=STAGES[5],
                permission=['app.can_transcribe_file'])
    def dispatch_qa(self, user=None):

        """"changes  file stage to QA

                    -records this action in Modification Table
                                         """
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[4],
            modified_to_stage=STAGES[5],
            by=user
        )
        self.flagged = False
        self.save()

    @transition(field=stage, source=[STAGES[5]], target=STAGES[4],
                permission=['app.can_qa_file'])
    def return_transcriber(self, user=None, rejection_comment=None):

        """"flags a  file stage to TRANSCRIBER

                            -records this action in Modification Table
                            -notify user who edited at reception
                            -notify all admins
                                                 """
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[5],
            modified_to_stage=STAGES[4],
            by=user
        )

        notification = Notification.objects.create(
            file=self,
            comment=rejection_comment
        )
        # user who did reception
        modified = Modification.objects.filter(modified_to_stage=STAGES[4]).last()
        if modified:
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
        if modified:
            self.assigned_to = modified.by
        else:
            self.assigned_to = None
        self.flagged = True
        self.save()

    @transition(field=stage, source=[STAGES[5]], target=STAGES[6],
                permission=['app.can_qa_file'])
    def dispatch_validator(self, user=None):
        """"changes  file stage to VALIDATOR

                    -records this action in Modification Table
                                         """

        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[5],
            modified_to_stage=STAGES[6],
            by=user
        )
        self.flagged = False
        self.save()

    @transition(field=stage, source=[STAGES[6]], target=STAGES[5],
                permission=['app.can_validate_file'])
    def return_qa(self, user=None, rejection_comment=None):

        """"flags a  file stage to QA

                            -records this action in Modification Table
                            -notify user who edited at reception
                            -notify all admins
                                                 """
        Modification.objects.create(
            file=self,
            modified_from_stage=STAGES[6],
            modified_to_stage=STAGES[5],
            by=user
        )

        notification = Notification.objects.create(
            file=self,
            comment=rejection_comment
        )
        # user who did reception
        modified = Modification.objects.filter(modified_to_stage=STAGES[5]).last()
        if modified:
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
        if modified:
            self.assigned_to = modified.by
        else:
            self.assigned_to = None
        self.flagged = True
        self.save()

    @transition(field=stage, source=[STAGES[6]], target=STAGES[1],
                permission=['app.can_validate_file'])
    def finalize_to_reception(self):
        self.flagged = False
        self.save()


class DocumentFileDetail(models.Model):
    file_reference = models.ForeignKey(DocumentFile, db_column="file_reference", on_delete=models.CASCADE, null=True)
    document_barcode = models.CharField(unique=True, max_length=255)

    document_name = models.CharField(max_length=255, blank=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True)

    document_content = JSONField(null=True)
    document_file_path = models.CharField(null=True, max_length=100)
    doc_created_by = models.ForeignKey(User, null=True, blank=True,
                                       on_delete=models.DO_NOTHING,
                                       related_name='doc_created_by')
    created_on = models.DateTimeField(auto_now_add=timezone.now)
    flagged = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.DO_NOTHING,
                                    related_name='doc_assigned_to')
    state = FSMField(default=STATES[0], protected=True)
    passed_qa = models.BooleanField(default=False)
    passed_validated = models.BooleanField(default=False)
    # transition methods
    @transition(field=state, source=[STATES[2]], target=STATES[0])
    def open(self):
        """"changes  document state to Open


                                                 """

    @transition(field=state, source=[STATES[0]], target=STATES[1], )
    def done(self):
        """"changes  document state to Done


                                                         """

    @transition(field=state, source=[STATES[1]], target=STATES[0], )
    def continue_editing(self):
        """"changes  document state  back to Open


                                                         """

    @transition(field=state, source=STATES[1], target=STATES[2])
    def close(self):
        """"changes  document state to Close


                                                         """
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

    file = models.ForeignKey(DocumentFile, on_delete=models.CASCADE)
    modified_from_stage = FSMField(null=False, protected=True)
    modified_to_stage = FSMField(null=True, protected=True)
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=timezone.now)


class Notification(models.Model):
    """all notifications"""

    file = models.ForeignKey(DocumentFile, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now)


class NotificationSentTo(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    read_at = models.DateTimeField(null=True)
