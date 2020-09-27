from django.contrib import admin
from .models import productItem, tfData

# Register your models here.
class productAdmin(admin.ModelAdmin):
    pass
admin.site.register(productItem,productAdmin)

class tfAdmin(admin.ModelAdmin):
    pass
admin.site.register(tfData,tfAdmin)