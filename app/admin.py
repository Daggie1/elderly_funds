from django.contrib import admin
from .models import Profile,Batch,DocumentFile,DocumentFileDetail,DocumentState

# Register your models here.
admin.site.register(Profile)
admin.site.register(Batch)
admin.site.register(DocumentFile)
admin.site.register(DocumentFileDetail)
admin.site.register(DocumentState)
