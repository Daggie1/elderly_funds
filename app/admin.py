from django.contrib import admin
from .models import Profile,Batch,DocumentFile,DocumentFileDetail,Modification,Notification

# Register your models here.
admin.site.register(Profile)
admin.site.register(Batch)
admin.site.register(DocumentFile)
admin.site.register(DocumentFileDetail)

admin.site.register(Modification)
admin.site.register(Notification)
