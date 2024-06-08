from django.db import models
from userauths.models import User
from django.utils import timezone

# Create your models he

class Wallet(models.Model):
    CURRENCY = (
        ('USD', 'Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'Pounds'),
        ('BRL', 'Brazilian real'),
        ('JPY', 'Japanese yen'),
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    balance = models.DecimalField(null=False, max_digits=10, decimal_places=2, editable=True)
    monthlyIncome = models.DecimalField(max_digits=7, decimal_places=2, editable=True)
    currencyType = models.CharField(max_length=3, null=False, choices=CURRENCY)
    

    def __str__(self):
        return str(self.balance)
    
class Transaction(models.Model):
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, null=False)
    value = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField(max_length=100)
    

    def __str__(self):
        return str(self.value)