from django.contrib import admin
from . import models

class SymbolAdmin(admin.ModelAdmin):
    list_display = ['exchange', 'symbol_name', 'last_price']

# Register your models here.


admin.site.register(models.Symbol, SymbolAdmin)

