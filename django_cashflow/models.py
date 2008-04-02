from django.db import models
from django.contrib.auth.models import User
from money.contrib.django.models.fields import MoneyField

__all__ = ('Account', 'Transaction',
		   'TX_ADD', 'TX_WITHDRAW', 'TX_MOVE',
		   'TX_CHOICES')

class Account(models.Model):
	number = models.CharField(max_length=80, primary_key=True)
	user = models.ForeignKey(User)
	balance = MoneyField(max_digits=12, decimal_places=2)
	description = models.TextField()
	
	modified = models.DateTimeField(auto_now=True, editable=False)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	
TX_ADD = 1
TX_WITHDRAW = 2
TX_MOVE = 3

TX_CHOICES = (
    (TX_ADD, 'add'),
    (TX_WITHDRAW, 'withdraw'),
    (TX_MOVE, 'move'),			 
)

class Transaction(models.Model):
	account = models.ForeignKey(Account)
	account_to = models.ForeignKey(Account, blank=True, null=True, related_name='move_transactions')
	type = models.SmallIntegerField(choices=TX_CHOICES)
	amount = models.IntegerField()
	balance = models.IntegerField()
	description = models.TextField()
	
	created = models.DateTimeField(auto_now_add=True, editable=False)
