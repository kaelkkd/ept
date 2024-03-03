from django.db import models
from userauths.models import User

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
    balance = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    monthlySalary = models.DecimalField(max_digits=7, decimal_places=2)
    currencyType = models.CharField(max_length=3, null=False, choices=CURRENCY)
    

    def str(self) -> float:
        return self.balance
    
