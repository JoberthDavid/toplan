from django.db import models



class ModelFileCost(models.Model):

    SICRO = 'SC'
    SINAPI = 'SN'
    ANALITICO = 'AN'
    SINTETICO = 'SI'
    EQUIPAMENTO = 'EQ'
    MAODEOBRA = 'MO'
    MATERIAL = 'MA'

    ACRE = 'AC'
    ALAGOAS = 'AL'
    AMAPA = 'AP'
    AMAZONAS = 'AM'
    BAHIA = 'BA'
    CEARA = 'CE'
    DISTRITO_FEDERAL = 'DF'
    ESPIRITO_SANTO = 'ES'
    GOIAS = 'GO'
    MARANHAO = 'MA'
    MATO_GROSSO = 'MT'
    MATO_GROSSO_DO_SUL = 'MS'
    MINAS_GERAIS = 'MG'
    PARA = 'PA'
    PARAIBA = 'PB'
    PARANA = 'PR'
    PERNAMBUCO = 'PE'
    PIAUI = 'PI'
    RIO_DE_JANEIRO = 'RJ'
    RIO_GRANDE_DO_NORTE = 'RN'
    RIO_GRANDE_DO_SUL = 'RS'
    RONDONIA = 'RO'
    RORAIMA = 'RR'
    SANTA_CATARINA = 'SC'
    SAO_PAULO = 'SP'
    SERGIPE = 'SE'
    TOCANTINS = 'TO'

    UF = [
        (ACRE, 'AMAZONAS'),
        (ALAGOAS, 'ALAGOAS'),
        (AMAPA, 'AMAPÁ'),
        (AMAZONAS, 'AMAZONAS'),
        (BAHIA, 'BAHIA'),
        (CEARA, 'CEARÁ'),
        (DISTRITO_FEDERAL, 'DISTRITO FEDERAL'),
        (ESPIRITO_SANTO, 'ESPÍRITO SANTO'),
        (GOIAS, 'GOIÁS'),
        (MARANHAO, 'MARANHÃO'),
        (MATO_GROSSO, 'MATO GROSSO'),
        (MATO_GROSSO_DO_SUL, 'MATO GROSSO DO SUL'),
        (MINAS_GERAIS, 'MINAS GERAIS'),
        (PARA, 'PARÁ'),
        (PARAIBA, 'PARAÍBA'),
        (PARANA, 'PARANÁ'),
        (PERNAMBUCO, 'PERNAMBUCO'),
        (PIAUI, 'PIAUÍ'),
        (RIO_DE_JANEIRO, 'RIO DE JANEIRO'),
        (RIO_GRANDE_DO_NORTE, 'RIO GRANDE DO NORTE'),
        (RIO_GRANDE_DO_SUL, 'RIO GRANDE DO SUL'),
        (RONDONIA, 'RONDÔNIA'),
        (RORAIMA, 'RORAIMA'),
        (SANTA_CATARINA, 'SANTA CATARINA'),
        (SAO_PAULO, 'SÃO PAULO'),
        (SERGIPE, 'SERGIPE'),
        (TOCANTINS, 'TOCANTINS'),
    ]

    ARQUIVO = [
        (ANALITICO, 'ANALÍTICO'),
        (SINTETICO, 'SINTÉTICO'),
        (EQUIPAMENTO, 'EQUIPAMENTO'),
        (MAODEOBRA, 'MÃO DE OBRA'),
        (MATERIAL, 'MATERIAL'),
    ]

    METODOLOGIA= [
        (SICRO, 'SICRO'),
        (SINAPI, 'SINAPI'),
    ]


    methodology = models.CharField(
        max_length=2,
        choices=METODOLOGIA,
        default=SICRO,
    )
    data_base = models.DateField(auto_now=False, auto_now_add=False)
    file = models.FileField(upload_to='upload_app/pdf_uploaded/')
    uf = models.CharField(
        max_length=2,
        choices=UF,
        default=GOIAS,        
    )
    type_system = models.CharField(
        max_length=2,
        choices=METODOLOGIA,
        default=SICRO,
    )
    type_file = models.CharField(
        max_length=2,
        choices=ARQUIVO,
        default=ANALITICO,
    )


    def __str__ (self):
        return str(self.file)