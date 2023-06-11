from PyPDF2 import PdfReader
from decimal import Decimal

from upload_app.models import ModelFileCost, ModelComposition, ModelInput, CompositionStamp
from upload_app.usefuls.choices import ANALITICO, SINTETICO, EQUIPAMENTO, MAODEOBRA, MATERIAL, AUXILIAR, TEMPO_FIXO, TRANSPORTE
from upload_app.usefuls.pattern import *
from upload_app.usefuls.regex_pattern import CompositionRegex

import timeit


class FileProcessor:
        
    def __init__(self, selected_object: ModelFileCost) -> None:
        self.selected_object = selected_object
        inicio = timeit.default_timer()
        self.access_file()
        fim = timeit.default_timer()
        print ('* => access_file : duracao de %f segundos' % (fim - inicio))
        self.extract_text_from_pdf_file()

    def access_file(self) -> None:
        with self.selected_object.file.open(mode="rb") as openned_file:
            self.pdf_content = PdfReader(openned_file)

    def get_list_of_inputs_of_composition(self, page_selected: int) -> list:
        return self.pdf_content.pages[ page_selected ].extract_text().split('\n')

    def switch_type_file(self, case):
        if case == ANALITICO:
            regex = CompositionRegex()

            composition_bulk_create_list = []
            input_bulk_create_list = []

            pages = len( self.pdf_content.pages )
            minimo = None
            maximo = None
            inicio1 = timeit.default_timer()
            page_dict = {}

            for page in range(pages):
                composition_object = CompositionStamp()
                inicio = timeit.default_timer()
                list_of_inputs_of_composition = self.get_list_of_inputs_of_composition( page )
                page_dict[page] = list_of_inputs_of_composition
                fim = timeit.default_timer()
                duracao = fim - inicio
                if minimo == None:
                    minimo = duracao
                elif minimo > duracao:
                    minimo = duracao
                if maximo == None:
                    maximo = duracao
                elif maximo < duracao:
                    maximo = duracao

                i = 0

                while i < 5:
                    row = list_of_inputs_of_composition[i]

                    if regex.switch_regex( FIC_REGEX, row) != None:
                        fic_str = regex.switch_regex( FIC_REGEX, row)
                        composition_object.fic = Decimal( fic_str.replace(".","").replace(",",".") )
                        
                    elif regex.switch_regex( DATA_BASE_REGEX, row) != None:
                        prod_str = regex.switch_regex( PRODUCTION_REGEX, row)
                        composition_object.production = Decimal( prod_str.replace(".","").replace(",",".") )
                        composition_object.unit = regex.switch_regex( UNIT_REGEX, row)
                        
                    elif regex.switch_regex( COMPOSITION_CODE_REGEX, row) != None:
                        composition_object.composition_code = regex.switch_regex( COMPOSITION_CODE_REGEX, row)
                    

                    i = i + 1

                composition_bulk_create_list.append(
                    ModelComposition(
                        composition_code=composition_object.composition_code,
                        fic=composition_object.fic,
                        production=composition_object.production,
                        file_cost=self.selected_object,
                        main_composition_group=composition_object.composition_code[0:2],
                    )
                )
            fim1 = timeit.default_timer()
            print ('* => get_list_of_inputs_of_composition : minima duracao de {} segundos; maxima duracao de {} segundos'.format(minimo, maximo))
            print ('* => primeiro for ModelComposition : duracao de %f segundos' % (fim1 - inicio1))

            list_of_composition_objects = ModelComposition.objects.bulk_create( composition_bulk_create_list )

            list_of_inputs = []
            list_of_inputs_x = []
            
            inicio2 = timeit.default_timer()
            for page in range(pages):
                composition_object = CompositionStamp()
                list_of_inputs_of_composition = page_dict[page]#self.get_list_of_inputs_of_composition( page )
                i = 0

                while i < len(list_of_inputs_of_composition):
                    row = list_of_inputs_of_composition[i]

                    if regex.switch_regex( EQUIPEMENT_CODE_REGEX, row ) != None:
                        code = regex.switch_regex( EQUIPEMENT_CODE_REGEX, row )
                        input_object = ModelInput(
                            main_input_code=code,
                            main_input_group=EQUIPAMENTO,
                            main_input_quantity=Decimal( regex.switch_regex( EQUIPEMENT_QUANT_REGEX, row ).replace(".","").replace(",",".") ),
                            main_input_use=Decimal( regex.switch_regex( EQUIPEMENT_UTIL_REGEX, row ).replace(".","").replace(",",".") ),
                            transported_input_code=None,
                            related_composition=list_of_composition_objects[page],
                        )
                        input_bulk_create_list.append( input_object )
                        list_of_inputs.append( code )

                    elif regex.switch_regex( EQUIPEMENT_QUANT_REGEX_ALFA, row ) != None:
                        composition_object.list_of_equipement_quantities.append( Decimal( regex.switch_regex( EQUIPEMENT_QUANT_REGEX_ALFA, row ).replace(".","").replace(",",".") ) )
                        composition_object.list_of_equipement_utilities.append( Decimal( regex.switch_regex( EQUIPEMENT_UTIL_REGEX_ALFA, row ).replace(".","").replace(",",".") ) )
                    
                    elif regex.switch_regex( EQUIPEMENT_CODE_REGEX_BETA, row ) != None:
                        codex = regex.switch_regex( EQUIPEMENT_CODE_REGEX_BETA, row )
                        list_of_inputs_x.append( codex )

                        # print( codex )

                        composition_object.list_of_equipement_codes.append( codex )

                    elif regex.switch_regex( FIXED_UNIT_REGEX, row ) != None:
                        code = regex.switch_regex( FIXED_CODE_REGEX, row )
                        input_object = ModelInput(
                            main_input_code=code,
                            main_input_group=TEMPO_FIXO,
                            main_input_quantity=Decimal( regex.switch_regex( FIXED_MATERIAL_QUANT_REGEX, row ).replace(".","").replace(",",".") ),
                            main_input_use=None,
                            transported_input_code=regex.switch_regex( FIXED_MATERIAL_CODE_REGEX, row ),
                            related_composition=list_of_composition_objects[page],
                        )
                        input_bulk_create_list.append( input_object )
                        list_of_inputs.append( code )

                    elif regex.switch_regex( TRANSPORTATION_UNIT_REGEX, row ) != None:
                        code = regex.switch_regex( TRANSPORTATION_PV_CODE_REGEX, row )
                        input_object = ModelInput(
                            main_input_code=code,
                            main_input_group=TRANSPORTE,
                            main_input_quantity=Decimal( regex.switch_regex( TRANSPORTATION_MATERIAL_QUANT_REGEX, row ).replace(".","").replace(",",".") ),
                            main_input_use=None,
                            transported_input_code=regex.switch_regex( TRANSPORTATION_MATERIAL_CODE_REGEX, row ),
                            related_composition=list_of_composition_objects[page],
                        )
                        input_bulk_create_list.append( input_object )
                        list_of_inputs.append( code )

                        code = regex.switch_regex( TRANSPORTATION_RP_CODE_REGEX, row )
                        input_object = ModelInput(
                            main_input_code=code,
                            main_input_group=TRANSPORTE,
                            main_input_quantity=Decimal( regex.switch_regex( TRANSPORTATION_MATERIAL_QUANT_REGEX, row ).replace(".","").replace(",",".") ),
                            main_input_use=None,
                            transported_input_code=regex.switch_regex( TRANSPORTATION_MATERIAL_CODE_REGEX, row ),
                            related_composition=list_of_composition_objects[page],
                        )
                        input_bulk_create_list.append( input_object )
                        list_of_inputs.append( code )

                        code = regex.switch_regex( TRANSPORTATION_LN_CODE_REGEX, row )
                        input_object = ModelInput(
                            main_input_code=code,
                            main_input_group=TRANSPORTE,
                            main_input_quantity=Decimal( regex.switch_regex( TRANSPORTATION_MATERIAL_QUANT_REGEX, row ).replace(".","").replace(",",".") ),
                            main_input_use=None,
                            transported_input_code=regex.switch_regex( TRANSPORTATION_MATERIAL_CODE_REGEX, row ),
                            related_composition=list_of_composition_objects[page],
                        )
                        input_bulk_create_list.append( input_object )
                        list_of_inputs.append( code )

                    elif regex.switch_regex( TRANSPORTATION_FE_CODE_REGEX_ALFA, row ) != None:
                        code = regex.switch_regex( TRANSPORTATION_FE_CODE_REGEX_ALFA, row )
                        input_object = ModelInput(
                            main_input_code=code,
                            main_input_group=TRANSPORTE,
                            main_input_quantity=Decimal( regex.switch_regex( TRANSPORTATION_MATERIAL_QUANT_REGEX_ALFA, row ).replace(".","").replace(",",".") ),
                            main_input_use=None,
                            transported_input_code=regex.switch_regex( TRANSPORTATION_MATERIAL_CODE_REGEX_ALFA, row ),
                            related_composition=list_of_composition_objects[page],
                        )
                        input_bulk_create_list.append( input_object )
                        list_of_inputs.append( code )

                    elif regex.switch_regex( GENERAL_INPUT_CODE_REGEX, row ) != None:
                        code = regex.switch_regex( GENERAL_INPUT_CODE_REGEX, row )

                        if regex.switch_regex( GENERAL_INPUT_CODE_REGEX, row )[0] == 'P':
                            group = MAODEOBRA
                        elif regex.switch_regex( GENERAL_INPUT_CODE_REGEX, row )[0] == 'M':
                            group = MATERIAL
                        else:
                            group = AUXILIAR

                        input_object = ModelInput(
                            main_input_code=code,
                            main_input_group=group,
                            main_input_quantity=Decimal( regex.switch_regex( GENERAL_INPUT_QUANT_REGEX, row ).replace(".","").replace(",",".") ),
                            main_input_use=None,
                            transported_input_code=None,
                            related_composition=list_of_composition_objects[page],
                        )
                        input_bulk_create_list.append( input_object )
                        list_of_inputs.append( code )

                    elif regex.switch_regex( GENERAL_INPUT_QUANT_REGEX_ALFA, row ) != None:
                        composition_object.list_of_general_input_quantities.append( Decimal( regex.switch_regex( GENERAL_INPUT_QUANT_REGEX_ALFA, row ).replace(".","").replace(",",".") ) )
                        composition_object.list_of_general_input_utilities.append( None )

                    elif regex.switch_regex( GENERAL_INPUT_CODE_REGEX_BETA, row ) != None:
                        composition_object.list_of_general_input_codes.append( regex.switch_regex( GENERAL_INPUT_CODE_REGEX_BETA, row ) )

                        if regex.switch_regex( GENERAL_INPUT_CODE_REGEX_BETA, row )[0] == 'P':
                            group = MAODEOBRA
                        elif regex.switch_regex( GENERAL_INPUT_CODE_REGEX_BETA, row )[0] == 'M':
                            group = MATERIAL
                        else:
                            group = AUXILIAR

                        composition_object.list_of_general_input_group.append( group )
                    
                    elif regex.switch_regex( BREAK_REGEX, row ) != None:
                        i = i + 6 #dont parse lastest rows of inputs

                    elif regex.switch_regex( LAST_REGEX, row ) != None:
                        composition_object.stop_flag = True
                    
                    i = i + 1
                    

            a = ModelInput.objects.bulk_create( input_bulk_create_list )
            fim2 = timeit.default_timer()
            print ('* => segundo for ModelInput : duracao de %f segundos' % (fim2 - inicio2))

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
        inicio = timeit.default_timer()
        self.switch_type_file( self.selected_object.type_file )
        fim = timeit.default_timer()
        print ('* => extract_text_from_pdf : duracao total de %f segundos' % (fim - inicio))