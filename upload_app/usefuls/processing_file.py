# import PyPDF2
# from upload_app.models import ModelFileCost
# from django.contrib import admin


# def processing_file(modeladmin, request, queryset):
#     # try:
#     selected_object = queryset.filter(status=False).first()
        
#     pdf_path = selected_object.file

#     with pdf_path.open(mode="rb") as f:
#         pdf_content = PyPDF2.PdfReader(f)

#         for page in pdf_content.pages:
#             print(page.extract_text())

#     selected_object.status=True
#     selected_object.save()


#     # except:
#     #     pass





# processing_file.short_description = 'Processar arquivo'