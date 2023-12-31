from django.contrib import admin
from .models import (Company, FinancialData, ExpenseCategory, Expense )
# Register your models here.

admin.site.register(Company)
admin.site.register(ExpenseCategory)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['company_id', 'category_id', ]
    list_filter = ['category_id']

@admin.register(FinancialData)
class FinancialDataAdmin(admin.ModelAdmin):
    list_display = ['company_id', 'year', 'revenue', 'total_sale', 'total_expense', 'net_income', 'current_ratio', 'debt_to_equity_ratio' ]
    list_filter = ['company_id', 'year']


