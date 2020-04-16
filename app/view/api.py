from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from app.serializers import DocumentSerializer

from app.models import DocumentFileDetail

@csrf_exempt
class ApiViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DocumentFileDetail.objects.all()
    serializer_class = DocumentSerializer