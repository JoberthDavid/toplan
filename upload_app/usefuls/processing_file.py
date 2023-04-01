# import pdftotext
# from upload_app.models import ModelFileCost


# def processing_file(modeladmin, request, queryset):
#     queryset = ModelFileCost.objects.filter(status=False)
#     for file_in_field in queryset:
        
#         if file_in_field.type_file == "AN":
#             path = file_in_field.file

#             with path.open(mode="rb") as f:
#                 pdf = pdftotext.PDF(f)
#                 num_pages = len(pdf)
                
#                 print(type(pdf))
#                 print(num_pages)
#         else:
#             print("*** Arquivo errado ***")

# processing_file.short_description = 'Processar arquivo'