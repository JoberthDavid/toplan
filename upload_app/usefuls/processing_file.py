import PyPDF2

from upload_app.models import ModelFileCost, CompositionModel
from upload_app.usefuls.choices import ANALITICO, SINTETICO, EQUIPAMENTO, MAODEOBRA, MATERIAL
from upload_app.usefuls.pattern import *
from upload_app.usefuls.regex_pattern import CompositionRegex


class FileProcessor:
        
    def __init__(self, selected_object: ModelFileCost) -> None:
        self.selected_object = selected_object
        self.access_file()
        self.extract_text_from_pdf_file()

    def access_file(self):
        with self.selected_object.file.open(mode="rb") as openned_file:
            self.pdf_content = PyPDF2.PdfReader(openned_file)

    def get_list_of_composition_header_rows(self):
        return self.pdf_content.pages[4501].extract_text().split('\n')[1:4]

    def get_list_of_inputs_of_composition(self):
        return self.pdf_content.pages[4501].extract_text().split('\n')[6:]

    def switch_type_file(self, case):
        if case == ANALITICO:
            regex = CompositionRegex()
            service = CompositionModel()
            for row in self.get_list_of_composition_header_rows():
                # print( row )
                if regex.switch_regex( FIC_REGEX, row) != None:
                    service.fic = regex.switch_regex( FIC_REGEX, row)
                elif regex.switch_regex( DATA_BASE_REGEX, row) != None:
                    service.data_base = regex.switch_regex( DATA_BASE_REGEX, row)
                    service.production = regex.switch_regex( PRODUCTION_REGEX, row)
                    service.unit = regex.switch_regex( UNIT_REGEX, row)
                elif regex.switch_regex( COMPOSITION_CODE_REGEX, row) != None:
                    service.composition_code = regex.switch_regex( COMPOSITION_CODE_REGEX, row)

            for row in self.get_list_of_inputs_of_composition():
                # print( row )
                equipement_code = regex.switch_regex( EQUIPAMENT_CODE_REGEX, row )
                equipament_quant = regex.switch_regex( EQUIPAMENT_QUANT_REGEX, row )
                equipament_util = regex.switch_regex( EQUIPAMENT_UTIL_REGEX, row )
                workmanship_code = regex.switch_regex( WORKMANSHIP_CODE_REGEX, row )
                workmanship_quant = regex.switch_regex( WORKMANSHIP_QUANT_REGEX, row )


            print(service.get_basic_data())

            # workmanship_break = None
            # list_of_inputs_of_composition = self.get_list_of_inputs_of_composition()
            # i = 0
            # while workmanship_break == None:
            #     row = list_of_inputs_of_composition[i]
            #     print( row )
            #     equipement_code = regex.switch_regex( EQUIPAMENT_CODE_REGEX, row )
            #     equipament_quant = regex.switch_regex( EQUIPAMENT_QUANT_REGEX, row )
            #     equipament_util = regex.switch_regex( EQUIPAMENT_UTIL_REGEX, row )
            #     workmanship_code = regex.switch_regex( WORKMANSHIP_CODE_REGEX, row )
            #     workmanship_quant = regex.switch_regex( WORKMANSHIP_QUANT_REGEX, row )
            #     workmanship_break = regex.switch_regex( WORKMANSHIP_BREAK_REGEX, row )

            #     # print(equipement_code)
            #     # print(equipament_quant)
            #     # print(equipament_util)
            #     # print(workmanship_code)
            #     # print(workmanship_quant)
            #     i = i + 1


        elif case == SINTETICO:
            print('Sintético')
        elif case == EQUIPAMENTO:
            for page in self.pdf_content.pages:
                print(page.extract_text())
        elif case == MAODEOBRA:
            print('Mão de obra')   
        elif case == MATERIAL:
            print('Material')  

    def extract_text_from_pdf_file(self):
        self.switch_type_file( self.selected_object.type_file )