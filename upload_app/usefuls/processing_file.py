import PyPDF2
from upload_app.models import ModelFileCost


def processing_file(modeladmin, request, queryset):
    queryset = ModelFileCost.objects.filter(status=False)
    for file_in_field in queryset:
        
        if file_in_field.type_file == "AN":
            path = file_in_field.file

            with path.open(mode="rb") as f:
                reader = PyPDF2.PdfReader(f)
                print(len(reader.pages))
                print(reader.pages[0].extract_text())
        else:
            pass




# import pdftotext
# def processing_file(modeladmin, request, queryset):
#     queryset = ModelFileCost.objects.filter(status=False)
#     for file_in_field in queryset:
        
#         if file_in_field.type_file == "AN":
#             path = file_in_field.file

#             with path.open(mode="rb") as f:
#                 pdf = pdftotext.PDF(f)
#                 num_pages = len(pdf)
#                 print(num_pages)
#                 print(pdf[0])
#         else:
#             pass

processing_file.short_description = 'Processar arquivo'