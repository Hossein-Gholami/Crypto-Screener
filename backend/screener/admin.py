from django.contrib import admin
from . import models

class SymbolAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

# Register your models here.


admin.site.register(models.Symbol, SymbolAdmin)

