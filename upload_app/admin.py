import PyPDF2

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from upload_app.models import ModelFileCost

from django.contrib import messages
from django.utils.translation import ngettext

from upload_app.usefuls.processing_file import FileProcessor


class ModelFileCostAdmin(admin.ModelAdmin):
    list_display = [ '_data_base', str, 'status']
    order_by = 'data_base'
    date_hierarchy = 'data_base'
    actions = ['process_file',]

    def select_object(self, queryset: QuerySet) -> ModelFileCost:
        return queryset.filter(status=False).first()

    def extract_text_from_pdf_file(self, selected_object: ModelFileCost) -> None:
        FileProcessor( selected_object )

    def update_selected_object(self, request: HttpRequest, selected_object: ModelFileCost) -> None:
        selected_object.status=True
        selected_object.save()
            
    def success_message_about_file_processing( self, request: HttpRequest, queryset: QuerySet) -> None:
        self.message_user( 
            request, 
            ngettext(
                "O arquivo selecionado foi processado.",
                "Apenas um arquivo foi processado de todos os selecionados.",
                len(queryset),
                ),
                messages.SUCCESS )

    def warning_message_about_file_processing( self, request: HttpRequest, queryset: QuerySet) -> None:
        self.message_user( 
            request, 
            ngettext(
                "O arquivo selecionado não foi processado.",
                "Os arquivos selecionados não foram processados.", 
                len(queryset),
                ),
                messages.WARNING )

    @admin.action(description='Processar arquivo')
    def process_file(self, request: HttpRequest, queryset: QuerySet) -> None:
        try:
            selected_object = self.select_object( queryset )
        
            self.extract_text_from_pdf_file( selected_object )

            self.update_selected_object( request, selected_object )
            
            self.success_message_about_file_processing( request, queryset )

        except:
            self.warning_message_about_file_processing( request, queryset )
            

admin.site.register(ModelFileCost, ModelFileCostAdmin)