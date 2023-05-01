import re
from typing import Match

from upload_app.usefuls.pattern import *


class CompositionRegex:

    def __init__( self ) -> None:
        self.first_row_pattern = FIRST_ROW_PATTERN

    def get_regex( self, pattern: str, evaluated: str, group: str ) -> str|None:
        if ( re.match( pattern, evaluated ) is not None ):
            chosen_regex = re.match( pattern, evaluated ).group( group )
        else:
            chosen_regex = None
        return chosen_regex

    def switch_regex(self, case: str, evaluated: str ) -> str:
        if case == FIC_REGEX:
            return self.get_regex( SECOND_ROW_PATTERN, evaluated, case )
        elif case == DATA_BASE_REGEX:
            return self.get_regex( THIRD_ROW_PATTERN, evaluated, case )
        elif case == PRODUCTION_REGEX:
            return self.get_regex( THIRD_ROW_PATTERN, evaluated, case )
        elif case == UNIT_REGEX:
            return self.get_regex( THIRD_ROW_PATTERN, evaluated, case )
        elif case == COMPOSITION_CODE_REGEX:
            return self.get_regex( FOURTH_ROW_PATTERN, evaluated, case )
        elif case == EQUIPEMENT_CODE_REGEX:
            return self.get_regex( EQUIPEMENT_PATTERN, evaluated, case )
        elif case == EQUIPEMENT_QUANT_REGEX:
            return self.get_regex( EQUIPEMENT_PATTERN, evaluated, case )
        elif case == EQUIPEMENT_UTIL_REGEX:
            return self.get_regex( EQUIPEMENT_PATTERN, evaluated, case )
        elif case == WORKMANSHIP_CODE_REGEX:
            return self.get_regex( WORKMANSHIP_PATTERN, evaluated, case )
        elif case == WORKMANSHIP_QUANT_REGEX:
            return self.get_regex( WORKMANSHIP_PATTERN, evaluated, case )
        elif case == MATERIAL_CODE_REGEX or case == MATERIAL_QUANT_REGEX:
            return self.get_regex( MATERIAL_PATTERN, evaluated, case )
        elif case == FIXED_CODE_REGEX or case == FIXED_MATERIAL_CODE_REGEX or case == FIXED_MATERIAL_QUANT_REGEX:
            return self.get_regex( FIXED_TIME_PATTERN, evaluated, case )
        elif case == BREAK_REGEX:
            return self.get_regex( BREAK_PATTERN, evaluated, case )
        elif case == LAST_REGEX:
            return self.get_regex( LAST_PATTERN, evaluated, case )



# class BodyCompositionRegex:

#     def __init__( self, pagina ) -> None:
#         self.linhas = self.obter_linhas( pagina )
#         self.regex_uf = ''
#         self.regex_fic = ''
#         self.regex_producao = ''
#         self.regex_codigo = ''
#         self.regex_EQUIPEMENTo = ''
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

#     def obter_pattern_EQUIPEMENTo( self ) -> str:
#         return r'(\s*) (?P<re_EQUIPEMENTo>[EA]\d{4}) (.+) (?P<re_quantidade>\d+\,\d{5}) (?P<re_utilizacao>\d+\,\d{2})'

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

#     def obter_regex_EQUIPEMENTo( self, range ) -> Match:
#         avaliado = self.linhas[ range ]
#         return re.match( self.obter_pattern_EQUIPEMENTo(), avaliado )

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
