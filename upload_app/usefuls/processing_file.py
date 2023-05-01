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

    def get_list_of_inputs_of_composition(self):
        return self.pdf_content.pages[4500].extract_text().split('\n')

    def switch_type_file(self, case):
        if case == ANALITICO:
            regex = CompositionRegex()
            composition_object = CompositionModel()
            list_of_inputs_of_composition = self.get_list_of_inputs_of_composition()
            i = 1 #jump first row of composition

            while composition_object.stop_flag == False:
                row = list_of_inputs_of_composition[i]
                if regex.switch_regex( FIC_REGEX, row) != None:
                    composition_object.fic = regex.switch_regex( FIC_REGEX, row)
                elif regex.switch_regex( DATA_BASE_REGEX, row) != None:
                    composition_object.data_base = regex.switch_regex( DATA_BASE_REGEX, row)
                    composition_object.production = regex.switch_regex( PRODUCTION_REGEX, row)
                    composition_object.unit = regex.switch_regex( UNIT_REGEX, row)
                elif regex.switch_regex( COMPOSITION_CODE_REGEX, row) != None:
                    composition_object.composition_code = regex.switch_regex( COMPOSITION_CODE_REGEX, row)
                elif regex.switch_regex( EQUIPEMENT_CODE_REGEX, row ) != None:
                    equipement_code = regex.switch_regex( EQUIPEMENT_CODE_REGEX, row )
                    equipement_quant = regex.switch_regex( EQUIPEMENT_QUANT_REGEX, row )
                    equipement_util = regex.switch_regex( EQUIPEMENT_UTIL_REGEX, row )
                    composition_object.list_of_equipement.append( ( equipement_code, equipement_quant, equipement_util ) )
                elif regex.switch_regex( WORKMANSHIP_CODE_REGEX, row ) != None:
                    workmanship_code = regex.switch_regex( WORKMANSHIP_CODE_REGEX, row )
                    workmanship_quant = regex.switch_regex( WORKMANSHIP_QUANT_REGEX, row )
                    composition_object.list_of_workmanship.append( ( workmanship_code, workmanship_quant ) )
                elif regex.switch_regex( MATERIAL_CODE_REGEX, row ) != None:
                    material_code = regex.switch_regex( MATERIAL_CODE_REGEX, row )
                    material_quant = regex.switch_regex( MATERIAL_QUANT_REGEX, row )
                    composition_object.list_of_materials.append( ( material_code, material_quant ) )
                elif regex.switch_regex( FIXED_CODE_REGEX, row ) != None:
                    fixed_code = regex.switch_regex( FIXED_CODE_REGEX, row )
                    fixed_material_code = regex.switch_regex( FIXED_MATERIAL_CODE_REGEX, row )
                    fixed_material_quant = regex.switch_regex( FIXED_MATERIAL_QUANT_REGEX, row )
                    composition_object.list_of_fixed_time.append( ( fixed_code, fixed_material_code, fixed_material_quant ) )
                elif regex.switch_regex( BREAK_REGEX, row ) != None:
                    i = i + 6 #jump costs of composition
                elif regex.switch_regex( LAST_REGEX, row ) != None:
                    composition_object.stop_flag = True
                i = i + 1

            # print( list_of_inputs_of_composition )
            print( composition_object.composition_code )
            print( composition_object.list_of_equipement)
            print( composition_object.list_of_workmanship)
            print( composition_object.list_of_materials)
            print( composition_object.list_of_fixed_time )
            # for item in list_of_inputs_of_composition:
            #     if regex.switch_regex( MATERIAL_CODE_REGEX, item ) != None:
            #         print( regex.switch_regex( MATERIAL_CODE_REGEX, item ) )


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