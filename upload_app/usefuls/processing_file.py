import PyPDF2
from decimal import Decimal

from upload_app.models import ModelFileCost, ModelComposition, ModelInput, CompositionStamp
from upload_app.usefuls.choices import ANALITICO, SINTETICO, EQUIPAMENTO, MAODEOBRA, MATERIAL
from upload_app.usefuls.pattern import *
from upload_app.usefuls.regex_pattern import CompositionRegex


class FileProcessor:
        
    def __init__(self, selected_object: ModelFileCost) -> None:
        self.selected_object = selected_object
        # print( "PK de ModelFileCost" + str(self.selected_object.pk) )
        self.access_file()
        self.extract_text_from_pdf_file()

    def access_file(self) -> None:
        with self.selected_object.file.open(mode="rb") as openned_file:
            self.pdf_content = PyPDF2.PdfReader(openned_file)
            # print( len( self.pdf_content.pages ) )

    def get_list_of_inputs_of_composition(self, page_selected: int) -> list:
        return self.pdf_content.pages[ page_selected ].extract_text().split('\n')

    def switch_type_file(self, case):
        if case == ANALITICO:
            regex = CompositionRegex()

            composition_bulk_list = []

            for page in range(90):#range( len( self.pdf_content.pages ) ):
                composition_object = CompositionStamp()
                list_of_inputs_of_composition = self.get_list_of_inputs_of_composition( page )
                i = 1 #jump first row of composition

                print( page )
                while i < len(list_of_inputs_of_composition):
                    row = list_of_inputs_of_composition[i]

                    if regex.switch_regex( FIC_REGEX, row) != None:
                        fic_str = regex.switch_regex( FIC_REGEX, row)
                        composition_object.fic = Decimal( fic_str.replace(".","").replace(",",".") )
                    elif regex.switch_regex( DATA_BASE_REGEX, row) != None:
                        prod_str = regex.switch_regex( PRODUCTION_REGEX, row)
                        composition_object.production = Decimal( prod_str.replace(".","").replace(",",".") )
                        composition_object.unit = regex.switch_regex( UNIT_REGEX, row)
                    elif regex.switch_regex( COMPOSITION_CODE_REGEX, row) != None:
                        composition_object.composition_code = int( regex.switch_regex( COMPOSITION_CODE_REGEX, row) )
                    elif regex.switch_regex( EQUIPEMENT_CODE_REGEX, row ) != None:
                        composition_object.list_of_equipement_codes.append( regex.switch_regex( EQUIPEMENT_CODE_REGEX, row ) )
                        composition_object.list_of_equipement_quantities.append( regex.switch_regex( EQUIPEMENT_QUANT_REGEX, row ) )
                        composition_object.list_of_equipement_utilities.append( regex.switch_regex( EQUIPEMENT_UTIL_REGEX, row ) )
                    elif regex.switch_regex( EQUIPEMENT_QUANT_REGEX_ALFA, row ) != None:
                        composition_object.list_of_equipement_quantities.append( regex.switch_regex( EQUIPEMENT_QUANT_REGEX_ALFA, row ) )
                        composition_object.list_of_equipement_utilities.append( regex.switch_regex( EQUIPEMENT_UTIL_REGEX_ALFA, row ) )
                    elif regex.switch_regex( EQUIPEMENT_CODE_REGEX_BETA, row ) != None:
                        composition_object.list_of_equipement_codes.append( regex.switch_regex( EQUIPEMENT_CODE_REGEX_BETA, row ) )
                    elif regex.switch_regex( FIXED_UNIT_REGEX, row ) != None:
                        composition_object.list_of_fixed_codes.append( regex.switch_regex( FIXED_CODE_REGEX, row ) )
                        composition_object.list_of_fixed_material_codes.append( regex.switch_regex( FIXED_MATERIAL_CODE_REGEX, row ) )
                        composition_object.list_of_fixed_material_quantities.append( regex.switch_regex( FIXED_MATERIAL_QUANT_REGEX, row ) )
                    elif regex.switch_regex( TRANSPORTATION_UNIT_REGEX, row ) != None:
                        composition_object.list_of_transp_pv_codes.append( regex.switch_regex( TRANSPORTATION_PV_CODE_REGEX, row ) )
                        composition_object.list_of_transp_rp_codes.append( regex.switch_regex( TRANSPORTATION_RP_CODE_REGEX, row ) )
                        composition_object.list_of_transp_ln_codes.append( regex.switch_regex( TRANSPORTATION_LN_CODE_REGEX, row ) )
                        composition_object.list_of_transp_material_codes.append( regex.switch_regex( TRANSPORTATION_MATERIAL_CODE_REGEX, row ) )
                        composition_object.list_of_transp_material_quantities.append( regex.switch_regex( TRANSPORTATION_MATERIAL_QUANT_REGEX, row ) )
                    elif regex.switch_regex( TRANSPORTATION_FE_CODE_REGEX_ALFA, row ) != None:
                        composition_object.list_of_transp_fe_codes.append( regex.switch_regex( TRANSPORTATION_FE_CODE_REGEX_ALFA, row ) )
                        composition_object.list_of_transp_material_codes.append( regex.switch_regex( TRANSPORTATION_MATERIAL_CODE_REGEX_ALFA, row ) )
                        composition_object.list_of_transp_material_quantities.append( regex.switch_regex( TRANSPORTATION_MATERIAL_QUANT_REGEX_ALFA, row ) )    
                    elif regex.switch_regex( GENERAL_INPUT_CODE_REGEX, row ) != None:
                        composition_object.list_of_general_input_codes.append( regex.switch_regex( GENERAL_INPUT_CODE_REGEX, row ) )
                        composition_object.list_of_general_input_quantities.append( regex.switch_regex( GENERAL_INPUT_QUANT_REGEX, row ) )
                    elif regex.switch_regex( GENERAL_INPUT_QUANT_REGEX_ALFA, row ) != None:
                        composition_object.list_of_general_input_quantities.append( regex.switch_regex( GENERAL_INPUT_QUANT_REGEX_ALFA, row ) )
                    elif regex.switch_regex( GENERAL_INPUT_CODE_REGEX_BETA, row ) != None:
                        composition_object.list_of_general_input_codes.append( regex.switch_regex( GENERAL_INPUT_CODE_REGEX_BETA, row ) )
                    elif regex.switch_regex( BREAK_REGEX, row ) != None:
                        i = i + 6 #jump costs of composition
                    elif regex.switch_regex( LAST_REGEX, row ) != None:
                        composition_object.stop_flag = True
                    i = i + 1

                    
                composition_bulk_list.append(
                    ModelComposition(
                        composition_code=composition_object.composition_code,
                        fic=composition_object.fic,
                        production=composition_object.production,
                        file_cost=self.selected_object
                        )
                    )
            
            ModelComposition.objects.bulk_create( composition_bulk_list )

            # print( composition_object.list_of_equipement_codes )
            # print( composition_object.list_of_equipement_quantities )
            # print( composition_object.list_of_equipement_utilities )
            # print( composition_object.list_of_general_input_codes)
            # print( composition_object.list_of_general_input_quantities)

            # print( composition_object.list_of_fixed_codes )
            # print( composition_object.list_of_fixed_material_codes )
            # print( composition_object.list_of_fixed_material_quantities )

            # print( composition_object.list_of_transp_pv_codes )
            # print( composition_object.list_of_transp_ln_codes )
            # print( composition_object.list_of_transp_rp_codes )
            # print( composition_object.list_of_transp_material_codes )
            # print( composition_object.list_of_transp_material_quantities )

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