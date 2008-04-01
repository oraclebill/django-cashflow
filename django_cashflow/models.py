from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from money.contrib.django.models.fields import MoneyField

__all__ = ('Account', 'Transaction')

DEFAULT_CURRENCY = settings.CASHFLOW_DEFAULT_CURRENCY

class Account(models.Model):
	user = models.ForeignKey(User)
	number = models.CharField(max_length=120)
	balance = MoneyField(max_digits=12, decimal_places=2, default_currency=DEFAULT_CURRENCY)
	description = models.TextField()
	
	modified = models.DateTimeField(auto_now=True, editable=False)
	created = models.DateTimeField(auto_now_add=True, editable=False)

class Transaction(models.Model):
	account = models.ForeignKey(Account)
	amount = MoneyField(max_digits=12, decimal_places=2, default_currency=DEFAULT_CURRENCY)
	balance = MoneyField(max_digits=12, decimal_places=2, default_currency=DEFAULT_CURRENCY)
	description = models.TextField()
	
	created = models.DateTimeField(auto_now_add=True, editable=False)
