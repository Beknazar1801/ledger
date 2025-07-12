from django.contrib import admin
from .models import BalanceItem, BalanceGroup, Account

admin.site.register(BalanceItem)
admin.site.register(BalanceGroup)
admin.site.register(Account)


from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'amount', 'debit_account', 'credit_account')
    list_filter = ('created_at',)
    search_fields = ('description',)
