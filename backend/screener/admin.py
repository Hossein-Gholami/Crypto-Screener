from django.contrib import admin
from . import models

class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['name']

# Register your models here.


admin.site.register(models.Exchange, ExchangeAdmin)

