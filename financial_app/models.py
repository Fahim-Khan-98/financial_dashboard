from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name


class ExpenseCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Expense(models.Model):
    expense_iD = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    category_id = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f'{self.company_id.company_name} {self.category_id.category_name} cost {self.amount}'
    


class FinancialData(models.Model):
    data_id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    year = models.IntegerField(blank=False)
    revenue = models.FloatField(blank=False)
    total_sale = models.FloatField(blank=True, null=True)
    net_income = models.FloatField(blank=True, null=True, editable=False)
    current_ratio = models.FloatField(editable=False)
    debt_to_equity_ratio = models.FloatField(editable=False)
    total_expense = models.FloatField(blank=True, null=True, editable=False)  # New field for total expense


    def __str__(self):
        return f'{self.company_id.company_name} {self.data_id} total expense {self.total_expense}'
    
    def calculate_expense(self):
        calculate_expense = Expense.objects.filter(company_id=self.company_id).aggregate(total=Sum('amount')).get('total', 0)
        return calculate_expense
    
    def calculate_expense_revenue(self):
        calculate_total_expense = self.revenue+self.calculate_expense()
        return calculate_total_expense

    
    def calculate_net_income(self):
        calculate_net_income = self.total_sale - self.calculate_expense_revenue()
        return calculate_net_income
    

    def calculate_current_ratio(self):
        calculate_current_ratio = self.total_sale / self.calculate_expense()
        return f'{calculate_current_ratio:2f}'
    
    def debit_equity_ratio(self):
        debit_equity_ratio =  self.calculate_expense()/ self.revenue
        return  f'{debit_equity_ratio:2f}'
    
    def save(self, *args, **kwargs):
        # Calculate total expense using the related Expense instances
        
        self.total_expense = self.calculate_expense_revenue()
        self.net_income = self.calculate_net_income()
        self.current_ratio = self.calculate_current_ratio()
        self.debt_to_equity_ratio = self.debit_equity_ratio()

        # Call the original save method
        super(FinancialData, self).save(*args, **kwargs)