from rest_framework.serializers import ModelSerializer
from upload_app.models import ModelFileCost, ModelComposition, ModelInput


class ModelFileCostSerializer(ModelSerializer):

    class Meta:
        model = ModelFileCost
        fields = ['id', 'methodology', 'data_base', 'file', 'uf', 'type_system', 'type_file']

class ModelInputSerializer(ModelSerializer):

    class Meta:
        model = ModelInput
        fields = ['id', 'related_composition', 'main_input_code', 'main_input_group', 'main_input_quantity', 'main_input_use', 'transported_input_code']


class ModelCompositionSerializer(ModelSerializer):

    modelinput_set = ModelInputSerializer(many=True, read_only=True)

    class Meta:
        model = ModelComposition
        fields = ['id', 'composition_code', 'fic', 'production', 'file_cost', 'modelinput_set']