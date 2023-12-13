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
    current_ratio = models.FloatField()
    debt_to_equity_ratio = models.FloatField()
    total_expense = models.FloatField(blank=True, null=True, editable=False)  # New field for total expense
    

    # def save(self, *args, **kwargs):
    #     # Calculate NetIncome before saving
    #     self.NetIncome = self.Revenue - self.Expenses
    #     super(FinancialData, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.company_id.company_name} {self.data_id} total expense {self.total_expense}'
    
    def calculate_expense(self):
        calculate_expense = Expense.objects.filter(company_id=self.company_id).aggregate(total=Sum('amount')).get('total', 0)
        return calculate_expense
    
    def calculate_total_expense(self):
        calculate_total_expense = self.revenue+self.calculate_expense()
        return calculate_total_expense

    
    def calculate_net_income(self):
        calculate_net_income = self.total_sale - self.calculate_total_expense()
        return calculate_net_income
    
    def save(self, *args, **kwargs):
        # Calculate total expense using the related Expense instances
        
        self.total_expense = self.calculate_total_expense()
        self.net_income = self.calculate_net_income()

        # Call the original save method
        super(FinancialData, self).save(*args, **kwargs)





# class MonthlyExpense(models.Model):
#     MonthlyExpenseID = models.AutoField(primary_key=True)
#     CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
#     ExpenseID = models.ForeignKey(Expense, on_delete=models.CASCADE)
#     Year = models.IntegerField()
#     Month = models.IntegerField()
#     Amount = models.FloatField()

#     def __str__(self):
#         return f'{self.CompanyID.CompanyName} {self.MonthlyExpenseID}'

# class YearlyExpense(models.Model):
#     YearlyExpenseID = models.AutoField(primary_key=True)
#     CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
#     ExpenseID = models.ForeignKey(Expense, on_delete=models.CASCADE)
#     Year = models.IntegerField()
#     Amount = models.FloatField()

#     def __str__(self):
#         return f'{self.CompanyID.CompanyName} {self.YearlyExpenseID}'
