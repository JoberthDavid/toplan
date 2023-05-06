from django.db import models
from django.core.validators import FileExtensionValidator

from upload_app.usefuls.choices import *


class ModelFileCost(models.Model):

    methodology = models.CharField(
        verbose_name="Metodologia",
        max_length=2,
        choices=METHODOLOGY,
        default=SICRO,
        )
    data_base = models.DateField(
        verbose_name="Data-base",
        auto_now=False, auto_now_add=False
        )
    file = models.FileField(
        verbose_name="Arquivo PDF",
        upload_to='upload_app/pdf_uploaded/',
        validators=[FileExtensionValidator(['pdf'])]
        )
    uf = models.CharField(
        verbose_name="UF",
        max_length=2,
        choices=UF,
        default=GOIAS,        
        )
    type_system = models.CharField(
        verbose_name="Tipo de sistema",
        max_length=2,
        choices=TYPE_SYSTEM,
        default=ONERADO,
        )
    type_file = models.CharField(
        verbose_name="Tipo de arquivo",
        max_length=2,
        choices=FILE,
        default=ANALITICO,
        )
    status = models.BooleanField(
        verbose_name="Arquivo processado",
        default=False,
    )


    class Meta:
        verbose_name="Arquivo de custo"

    def __str__(self):
        return "".join([self.methodology, " - ",self.uf, " - ", self.parser_data_base_to_string(), " - ", self.type_system, " - ", self.type_file])
    
    def format_data_base(self):
        return self.data_base.__format__("%m/%Y")

    def parser_data_base_to_string(self):
        return str(self.format_data_base())

    def get_absolute_url(self):
        return '/upload_app/%i/' % self.id
    

class CompositionModel:

    def __init__( self ) -> None:
        self.fic = None
        self.data_base = None
        self.production = None
        self.unit = None
        self.composition_code = None
        self.list_of_equipement_codes = []
        self.list_of_equipement_quantities = []
        self.list_of_equipement_utilities = []
        self.list_of_workmanship_codes = []
        self.list_of_workmanship_quantities = []
        self.list_of_material_codes = []
        self.list_of_material_quantities = []
        self.list_of_fixed_codes = []
        self.list_of_fixed_material_codes = []
        self.list_of_fixed_material_quantities = []

        self.list_of_auxiliaries_activities = []

        self.list_of_transp_pv_codes = []
        self.list_of_transp_ln_codes = []
        self.list_of_transp_rp_codes = []
        self.list_of_transp_material_codes = []
        self.list_of_transp_material_quantities = []
        
        self.stop_flag = False


    def get_basic_data(self):
        return str(self.composition_code) + str(self.fic) + str(self.data_base) + str(self.production) + str(self.unit)