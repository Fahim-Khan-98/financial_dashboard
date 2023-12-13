# dashboard_app/views.py
from rest_framework import generics, viewsets, permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from financial_app.models import Company, FinancialData
# , FinancialRatios, DashboardPreferences, ExpenseCategory, Expense, MonthlyExpense, YearlyExpense
from .serializers import (CompanySerializer, UserSerializer, FinancialDataSerializer)
# , FinancialDataSerializer, FinancialRatiosSerializer, DashboardPreferencesSerializer, ExpenseCategorySerializer, ExpenseSerializer, MonthlyExpenseSerializer, YearlyExpenseSerializer
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly, IsCompanyOwner



class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsOwnerOrReadOnly]

class FinancialDataList(generics.ListCreateAPIView):
    queryset = FinancialData.objects.all()
    serializer_class = FinancialDataSerializer

class FinancialDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FinancialData.objects.all()
    serializer_class = FinancialDataSerializer
    permission_classes = [IsOwnerOrReadOnly]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Assuming User model exists
    serializer_class = UserSerializer

class Analytics(APIView):
    def get_queryset(self):
        return FinancialData.objects.none()
    
    def get(self, request, *args, **kwargs):
        # Assuming 'year' is a query parameter in the request
        year = self.request.query_params.get('year', None)

        if not year:
            return Response({"error": "Year parameter is required."}, status=400)

        try:
            year = int(year)
        except ValueError:
            return Response({"error": "Invalid year parameter."}, status=400)

        # Get all financial data for the specified year
        financial_data = FinancialData.objects.filter(year=year)


        if not financial_data.exists():
            return Response({"error": f"No financial data available for the year {year}"}, status=404)

        # Calculate average Current Ratio and Debt-to-Equity Ratio
        total_current_ratio = 0
        total_debt_to_equity_ratio = 0
        num_companies = financial_data.count()

        for data in financial_data:
            total_current_ratio += data.current_ratio
            total_debt_to_equity_ratio += data.debt_to_equity_ratio

        # Avoid division by zero
        avg_current_ratio = total_current_ratio / num_companies if num_companies > 0 else 0
        avg_debt_to_equity_ratio = total_debt_to_equity_ratio / num_companies if num_companies > 0 else 0

        # Prepare response
        response_data = {
            "Year": year,
            "Revenue": data.revenue,
            "Total Expense": data.total_expense,
            "Total Sale": data.total_sale,
            "Net Income": data.net_income,
            "Average Current Ratio": avg_current_ratio,
            "Average Debt To Equity Ratio": avg_debt_to_equity_ratio,
        }

        return Response(response_data, status=200)

# Repeat the process for other views
#