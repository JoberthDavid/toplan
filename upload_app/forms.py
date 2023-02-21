from django.forms import ModelForm
from upload_app.models import ModelFileCost

class FormFileCost(ModelForm):

    class Meta:
        model = ModelFileCost
        fields = [ 'methodology', 'data_base', 'file', 'uf', 'type_system', 'type_file' ]