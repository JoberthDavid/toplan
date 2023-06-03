from rest_framework.viewsets import ModelViewSet
from upload_app.models import ModelFileCost, ModelComposition, ModelInput
from upload_app.api.serializers import ModelFileCostSerializer, ModelCompositionSerializer, ModelInputSerializer


class FileCostViewSet(ModelViewSet):

    queryset = ModelFileCost.objects.filter(status=True)
    serializer_class = ModelFileCostSerializer


class CompositionViewSet(ModelViewSet):

    queryset = ModelComposition.objects.all()
    serializer_class = ModelCompositionSerializer


class InputViewSet(ModelViewSet):

    queryset = ModelInput.objects.all()
    serializer_class = ModelInputSerializer