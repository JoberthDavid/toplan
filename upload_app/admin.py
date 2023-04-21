import PyPDF2

from django.contrib import admin
from upload_app.models import ModelFileCost

from django.contrib import messages
from django.utils.translation import ngettext


class ModelFileCostAdmin(admin.ModelAdmin):
    list_display = [ '_data_base', str, 'status']
    order_by = 'data_base'
    date_hierarchy = 'data_base'
    actions = ['process_file',]

    def select_object(self, queryset):
        return queryset.filter(status=False).first()

    def extract_text_from_pdf_file(self, selected_object: ModelFileCost):
        with selected_object.file.open(mode="rb") as f:
            pdf_content = PyPDF2.PdfReader(f)

            for page in pdf_content.pages:
                print(page.extract_text())

    def update_selected_object(self, request, selected_object: ModelFileCost):
        selected_object.status=True
        selected_object.save()

        if selected_object != None and selected_object.status==True:
            self.message_about_file_processing( request )

    def message_about_file_processing( self, request ):
        self.message_user( 
            request, 
            ngettext(
                "O arquivo selecionado foi processado.",
                "Os arquivos selecionados foram processados.", 
                1,
                ),
                messages.SUCCESS )


    @admin.action(description='Processar arquivo')
    def process_file(self, request, queryset):
        try:
            selected_object = self.select_object( queryset )
        
            self.extract_text_from_pdf_file( selected_object )

            self.update_selected_object( request, selected_object )

        except:
            pass


admin.site.register(ModelFileCost, ModelFileCostAdmin)