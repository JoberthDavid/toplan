from rest_framework.serializers import ModelSerializer
from upload_app.models import ModelInput

class ModelInputSerializer(ModelSerializer):

    class Meta:
        model = ModelInput
        fields = ('id', 'main_input_code', 'main_input_group', 'main_input_quantity', 'main_input_use', 'transported_input_code', 'related_composition')