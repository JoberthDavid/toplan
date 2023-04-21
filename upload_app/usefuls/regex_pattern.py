import re
from typing import Match


class HeaderCompositionRegex:

    def __init__( self, evaluated: str ) -> None:
        first_row_of_header = r'(        Valores em reais (R$)Custo Unitário de Referência Produção da equipe)'
        second_row_of_header = r'(.*) (Amazonas|Alagoas|Amapá|Bahia|Ceará|Distrito Federal|Espírito Santo|Goiás|Maranhão|Mato Grosso|Mato Grosso do Sul|Minas Gerais|Pará|Paraíba|Paraná|Pernambuco|Piauí|Rio de Janeiro|Rio Grande do Norte|Rio Grande do Sul|Rondônia|Roraima|Santa Catarina|São Paulo|Sergipe|Tocantins) (SISTEMA DE CUSTOS REFERENCIAIS DE OBRAS - SICRO) ?(FIC) ?(?P<fic_regex>\d\,\d\d\d\d\d) (CGCIT DNIT)'
        third_row_of_header = r'(?P<data_base_regex>Janeiro|Fevereiro|Março|Abril|Maio|Junho|Julho|Agosto|Setembro|Outubro|Novembro|Dezembro\/\d{4}) (?P<production_regex>\d{1,3}(\.\d{3})*,\d{5}) (?P<unit_regex>.+)'
        fourth_row_of_header = r'(\d{7})'
        header_regex_list = [first_row_of_header, second_row_of_header, third_row_of_header, fourth_row_of_header]
        self.header = self.get_header_regex( evaluated, header_regex_list )

    def get_header_regex( self, evaluated: str, header_regex_list: list ):
        chosen_regex = {}
        for header_regex_option in header_regex_list:
            if ( re.match( header_regex_option, evaluated ) is not None ):
                chosen_regex = re.match( header_regex_option, evaluated )
        return chosen_regex


# class BodyCompositionRegex:

#     def __init__( self, pagina ) -> None:
#         self.linhas = self.obter_linhas( pagina )
#         self.regex_uf = ''
#         self.regex_fic = ''
#         self.regex_producao = ''
#         self.regex_codigo = ''
#         self.regex_equipamento = ''
#         self.regex_mao_de_obra = ''
#         self.regex_tempo_fixo = ''
#         self.regex_transporte_rodoviario = ''
#         self.regex_transporte_ferroviario = ''
#         self.regex_atividade_auxiliar = ''
#         self.regex_material = ''

#     def obter_linhas( self, pagina ) -> list:
#         aux1 = pagina
#         aux2 = ''
#         while aux1 != aux2:
#             aux2 = aux1
#             aux1 = aux1.replace('  ', ' ')
#         linhas = aux1.split('\n')
#         return linhas

#     def obter_pattern_fic( self ) -> str:
#         return r'(.+) (?P<re_uf>.+) (FIC) (?P<re_fic>\d\,\d\d\d\d\d)'

#     def obter_pattern_uf( self ) -> str:
#         return r'(SISTEMA DE CUSTOS REFERENCIAIS DE OBRAS - SICRO) (?P<re_uf>\w+)'

#     def obter_pattern_producao( self ) -> str:
#         return r'(.+) (?P<re_data_base>.+) (Produção da equipe) (?P<re_producao>\d{1,3}(\.\d{3})*,\d{5}) (?P<re_unidade>.+)'
    
#     def obter_pattern_codigo( self ) -> str:
#         return r'(?P<re_codigo>\d{7}) (.+) (Valores em reais \(R\$\))'

#     def obter_pattern_equipamento( self ) -> str:
#         return r'(\s*) (?P<re_equipamento>[EA]\d{4}) (.+) (?P<re_quantidade>\d+\,\d{5}) (?P<re_utilizacao>\d+\,\d{2})'

#     def obter_pattern_mao_de_obra( self ) -> str:
#         return r'(\s*) (?P<re_mao_de_obra>[P]\d{4}) (.+) (?P<re_quantidade>\d+\,\d{5})'

#     def obter_pattern_tempo_fixo( self ) -> str:
#         return r'(\s*) (?P<re_item_transportado>\d{7}|[M]\d{4}) (.+) (?P<re_tempo_fixo>59\d{5}){1} (?P<re_quantidade>\d+\,\d{5}) (t){1}'
    
#     def obter_pattern_transporte_rodoviario( self ) -> str:
#         return r'(\s*) (?P<re_item_transportado>\d{7}|[M]\d{4}) (.+) (?P<re_quantidade>\d+\,\d{5}) (tkm){1} (?P<re_leito_natural>59\d{5}) (?P<re_revestimento_primario>59\d{5}) (?P<re_pavimentado>59\d{5})'

#     def obter_pattern_transporte_ferroviario( self ) -> str:
#         return r'(\s*) (?P<re_item_transportado>\d{7}|[M]\d{4}) (.+) (?P<re_quantidade>\d+\,\d{5}) (tkm){1} (?P<re_ferroviario>59\d{5})'

#     def obter_pattern_atividade_auxiliar( self ) -> str:
#         return r'(\s*) (?P<re_atividade_auxiliar>\d{7}) (.+) (?P<re_quantidade>\d+\,\d{5}) (\w{1,3})'

#     def obter_pattern_material( self ) -> str:
#         return r'(\s*) (?P<re_material>[M]\d{4}) (.+) (?P<re_quantidade>\d+\,\d{5}) (\w{1,3})'

#     def obter_regex_fic( self, range ) -> Match:
#         avaliado = self.linhas[ range ]
#         return re.match( self.obter_pattern_fic(), avaliado )

#     def obter_regex_uf( self, range ) -> Match:
#         avaliado = self.linhas[ range ]
#         return re.match( self.obter_pattern_uf(), avaliado )

#     def obter_regex_producao( self, range ) -> Match:
#         avaliado = self.linhas[ range ]
#         return re.match( self.obter_pattern_producao(), avaliado )

#     def obter_regex_codigo( self, range ) -> Match:
#         avaliado = self.linhas[ range + 1]
#         return re.match( self.obter_pattern_codigo(), avaliado )

#     def obter_regex_equipamento( self, range ) -> Match:
#         avaliado = self.linhas[ range ]
#         return re.match( self.obter_pattern_equipamento(), avaliado )

#     def obter_regex_mao_de_obra( self, range ) -> Match:
#         avaliado = self.linhas[ range ]
#         return re.match( self.obter_pattern_mao_de_obra(), avaliado )

#     def obter_regex_tempo_fixo( self, range ) -> Match:
#         avaliado = self.linhas[ range ]
#         return re.match( self.obter_pattern_tempo_fixo(), avaliado )

#     def obter_regex_transporte_rodoviario( self, range ) -> Match:
#         avaliado = self.linhas[ range ]
#         return re.match( self.obter_pattern_transporte_rodoviario(), avaliado )

#     def obter_regex_transporte_ferroviario( self, range ) -> Match:
#         avaliado = self.linhas[ range ]
#         return re.match( self.obter_pattern_transporte_ferroviario(), avaliado )

#     def obter_regex_atividade_auxiliar( self, range ) -> Match:
#         avaliado = self.linhas[ range ]
#         return re.match( self.obter_pattern_atividade_auxiliar(), avaliado )

#     def obter_regex_material( self, range ) -> Match:
#         avaliado = self.linhas[ range ]
#         return re.match( self.obter_pattern_material(), avaliado )
