from django.db import models

# Create your models here.

class CurrencyRate(models.Model):
    currency_symbol = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=8)
    date = models.DateField()