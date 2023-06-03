from rest_framework.viewsets import ModelViewSet
from upload_app.models import ModelInput
from upload_app.api.serializers import ModelInputSerializer


class InputViewSet(ModelViewSet):

    queryset = ModelInput.objects.all()
    serializer_class = ModelInputSerializer