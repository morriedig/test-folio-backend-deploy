from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Portfolio)
admin.site.register(Stock)
admin.site.register(Transaction)
admin.site.register(Stockprice)
admin.site.register(Follow)
