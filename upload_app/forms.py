from django.forms import ModelForm
from upload_app.models import ModelFileCost


class FormFileCost(ModelForm):


    class Meta:
        model = ModelFileCost
        fields = '__all__'