from django.urls import path
from .views import (CompanyList, CompanyDetail, Analytics, UserViewSet
                    , FinancialDataList, FinancialDataDetail) 
# , FinancialDataList, FinancialDataDetail, FinancialRatiosList, FinancialRatiosDetail, DashboardPreferencesList, DashboardPreferencesDetail, ExpenseCategoryList, ExpenseCategoryDetail, ExpenseList, ExpenseDetail, MonthlyExpenseList, MonthlyExpenseDetail, YearlyExpenseList, YearlyExpenseDetail

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', CompanyList.as_view(), name='company-list'),
    path('companies/', CompanyList.as_view(), name='company-list'),
    path('companies/<int:pk>/', CompanyDetail.as_view(), name='company-detail'),
    path('financials/', FinancialDataList.as_view(), name='financials-list'),
    path('financials/<int:pk>/', FinancialDataDetail.as_view(), name='financials-detail'),
    path('analytics/', Analytics.as_view(), name='analytics'),
    # Define URLs for other views
]