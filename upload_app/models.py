from django.db import models
from django.core.validators import FileExtensionValidator

from upload_app.usefuls.choices import *

class ModelFileCost(models.Model):

    # SICRO = 'SC'
    # SINAPI = 'SN'
    # ANALITICO = 'AN'
    # SINTETICO = 'SI'
    # EQUIPAMENTO = 'EQ'
    # MAODEOBRA = 'MO'
    # MATERIAL = 'MA'
    # ONERADO = 'ON'
    # DESONERADO = 'DS'

    # ACRE = 'AC'
    # ALAGOAS = 'AL'
    # AMAPA = 'AP'
    # AMAZONAS = 'AM'
    # BAHIA = 'BA'
    # CEARA = 'CE'
    # DISTRITO_FEDERAL = 'DF'
    # ESPIRITO_SANTO = 'ES'
    # GOIAS = 'GO'
    # MARANHAO = 'MA'
    # MATO_GROSSO = 'MT'
    # MATO_GROSSO_DO_SUL = 'MS'
    # MINAS_GERAIS = 'MG'
    # PARA = 'PA'
    # PARAIBA = 'PB'
    # PARANA = 'PR'
    # PERNAMBUCO = 'PE'
    # PIAUI = 'PI'
    # RIO_DE_JANEIRO = 'RJ'
    # RIO_GRANDE_DO_NORTE = 'RN'
    # RIO_GRANDE_DO_SUL = 'RS'
    # RONDONIA = 'RO'
    # RORAIMA = 'RR'
    # SANTA_CATARINA = 'SC'
    # SAO_PAULO = 'SP'
    # SERGIPE = 'SE'
    # TOCANTINS = 'TO'

    # UF = [
    #     (ACRE, 'AMAZONAS'),
    #     (ALAGOAS, 'ALAGOAS'),
    #     (AMAPA, 'AMAPÁ'),
    #     (AMAZONAS, 'AMAZONAS'),
    #     (BAHIA, 'BAHIA'),
    #     (CEARA, 'CEARÁ'),
    #     (DISTRITO_FEDERAL, 'DISTRITO FEDERAL'),
    #     (ESPIRITO_SANTO, 'ESPÍRITO SANTO'),
    #     (GOIAS, 'GOIÁS'),
    #     (MARANHAO, 'MARANHÃO'),
    #     (MATO_GROSSO, 'MATO GROSSO'),
    #     (MATO_GROSSO_DO_SUL, 'MATO GROSSO DO SUL'),
    #     (MINAS_GERAIS, 'MINAS GERAIS'),
    #     (PARA, 'PARÁ'),
    #     (PARAIBA, 'PARAÍBA'),
    #     (PARANA, 'PARANÁ'),
    #     (PERNAMBUCO, 'PERNAMBUCO'),
    #     (PIAUI, 'PIAUÍ'),
    #     (RIO_DE_JANEIRO, 'RIO DE JANEIRO'),
    #     (RIO_GRANDE_DO_NORTE, 'RIO GRANDE DO NORTE'),
    #     (RIO_GRANDE_DO_SUL, 'RIO GRANDE DO SUL'),
    #     (RONDONIA, 'RONDÔNIA'),
    #     (RORAIMA, 'RORAIMA'),
    #     (SANTA_CATARINA, 'SANTA CATARINA'),
    #     (SAO_PAULO, 'SÃO PAULO'),
    #     (SERGIPE, 'SERGIPE'),
    #     (TOCANTINS, 'TOCANTINS'),
    # ]

    # ARQUIVO = [
    #     (ANALITICO, 'ANALÍTICO'),
    #     (SINTETICO, 'SINTÉTICO'),
    #     (EQUIPAMENTO, 'EQUIPAMENTO'),
    #     (MAODEOBRA, 'MÃO DE OBRA'),
    #     (MATERIAL, 'MATERIAL'),
    # ]

    # METODOLOGIA= [
    #     (SICRO, 'SICRO'),
    #     (SINAPI, 'SINAPI'),
    # ]

    # TIPO_SISTEMA=[
    #     (ONERADO, 'ONERADO'),
    #     (DESONERADO, 'DESONERADO'),
    # ]


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