from rest_framework.viewsets import ModelViewSet
from upload_app.models import ModelFileCost, ModelComposition, ModelInput
from upload_app.api.serializers import ModelFileCostSerializer, ModelCompositionSerializer, ModelInputSerializer


class FileCostViewSet(ModelViewSet):

    serializer_class = ModelFileCostSerializer

    def get_queryset(self):
        methodology = self.request.query_params.get('metodologia')
        type_system = self.request.query_params.get('sistema')
        data_base = self.request.query_params.get('data_base')

        queryset = ModelFileCost.objects.filter(status=True)

        if methodology:
            queryset = ModelFileCost.objects.filter(methodology=methodology)
        if type_system:
            queryset = ModelFileCost.objects.filter(type_system=type_system)
        if data_base:
            queryset = ModelFileCost.objects.filter(data_base=data_base)
            
        return queryset


class CompositionViewSet(ModelViewSet):

    serializer_class = ModelCompositionSerializer

    def get_queryset(self):
        methodology = self.request.query_params.get('metodologia')
        type_system = self.request.query_params.get('sistema')
        data_base = self.request.query_params.get('data_base')
        composition_code = self.request.query_params.get('composicao')

        queryset = ModelComposition.objects.all()

        if methodology:
            queryset = ModelComposition.objects.filter(file_cost__methodology=methodology)
        if type_system:
            queryset = ModelComposition.objects.filter(file_cost__type_system=type_system)
        if data_base:
            queryset = ModelComposition.objects.filter(file_cost__data_base=data_base)
        if composition_code:
            queryset = ModelComposition.objects.filter(composition_code=composition_code)

        return queryset


class InputViewSet(ModelViewSet):

    serializer_class = ModelInputSerializer

    def get_queryset(self):
        methodology = self.request.query_params.get('metodologia')
        type_system = self.request.query_params.get('sistema')
        data_base = self.request.query_params.get('data_base')
        composition_code = self.request.query_params.get('composicao')
        main_input_group = self.request.query_params.get('grupo')

        queryset = ModelInput.objects.all()

        if methodology:
            queryset = ModelInput.objects.filter(related_composition__file_cost__methodology=methodology)
        if type_system:
            queryset = ModelInput.objects.filter(related_composition__file_cost__type_system=type_system)
        if data_base:
            queryset = ModelInput.objects.filter(related_composition__file_cost__data_base=data_base)
        if composition_code:
            queryset = ModelInput.objects.filter(related_composition__composition_code=composition_code)
        if main_input_group:
            queryset = ModelInput.objects.filter(main_input_group=main_input_group)

        return queryset