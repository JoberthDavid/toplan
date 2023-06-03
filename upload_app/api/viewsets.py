from rest_framework.viewsets import ModelViewSet
from upload_app.models import ModelFileCost, ModelComposition, ModelInput
from upload_app.api.serializers import ModelFileCostSerializer, ModelCompositionSerializer, ModelInputSerializer


class FileCostViewSet(ModelViewSet):

    serializer_class = ModelFileCostSerializer

    def get_queryset(self):
        return ModelFileCost.objects.filter(status=True)


class CompositionViewSet(ModelViewSet):

    serializer_class = ModelCompositionSerializer

    def get_queryset(self):
        return ModelComposition.objects.filter(production=2.0)


class InputViewSet(ModelViewSet):

    serializer_class = ModelInputSerializer

    def get_queryset(self):
        return ModelInput.objects.filter(related_composition=83709)