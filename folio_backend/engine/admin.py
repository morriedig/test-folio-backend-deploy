from django.contrib import admin

# Register your models here.
from engine.models import Follow, Portfolio, Stock, Stockprice, Transaction, User

admin.site.register(Follow)
admin.site.register(Portfolio)
admin.site.register(Stock)
admin.site.register(Stockprice)
admin.site.register(Transaction)
admin.site.register(User)
