from django.contrib import admin

# Register your models here.
from .models import *


class idAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Portfolio, idAdmin)
admin.site.register(Stock, idAdmin)
admin.site.register(Transaction, idAdmin)
admin.site.register(Stockprice, idAdmin)
admin.site.register(Follow, idAdmin)
