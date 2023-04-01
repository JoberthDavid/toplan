from django.contrib import admin
from upload_app.models import ModelFileCost
# from .usefuls.processing_file import processing_file


# class ModelFileCostAdmin(admin.ModelAdmin):
#     actions = [processing_file,]

admin.site.register(ModelFileCost)#, ModelFileCostAdmin)