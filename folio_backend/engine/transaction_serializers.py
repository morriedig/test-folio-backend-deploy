# import json

# from django.core.serializers import serialize
# from django.db.models import Q
# from rest_framework.serializers import CharField, ValidationError

# from .models import Portfolio, Transaction

# ignore this, will refactor later

# class TransactionSerializer:
#     class Meta:
#         model = Transaction
#         fields = "__all__"


#     def get_by_period(self, id, start_date, end_date, reverse=True):
#         transactions = Transaction.objects.filter(
#             Q(portfolio__id = id) |
#             Q(time__range = (start_date, end_date))
#         )

#         if reverse:
#             transactions.order_by('-time')

#         return serialize(
#             "json",
#             transactions,
#             fields = ("portfolio", "stock", "amount", "time", "price")
#         )

#     def get_by_time_before(self, id, end_date):
#         transactions = Transaction.objects.filter(
#             Q(portfolio__id = id) |
#             Q(time__lt = end_date)
#         )

#         return serialize(
#             "json",
#             transactions,
#             fields = ("portfolio", "stock", "amount", "time", "price")
#         )

#     def get_all(self, id):
#         return serialize(
#             "json",
#             Transaction.objects.filter(portfolio__id = id),
#             fields = ("portfolio", "stock", "amount", "time", "price")
#         )
