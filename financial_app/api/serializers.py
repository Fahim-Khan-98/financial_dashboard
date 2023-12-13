# dashboard_app/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from financial_app.models import Company, FinancialData

# , FinancialRatios, DashboardPreferences, ExpenseCategory, Expense, MonthlyExpense, YearlyExpense

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

