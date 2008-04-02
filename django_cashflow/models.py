from django.db import models
from django.db.transaction import commit_on_success
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
	
	@commit_on_success
	def add_money(self, amount, description):
		self.balance += amount
		transaction = self._create_transaction(TX_ADD, amount, description)
		self.save()
		transaction.save()
	
	@commit_on_success
	def withdraw_money(self, amount, description):
		self.balance -= amount
		transaction = self._create_transaction(TX_WITHDRAW, amount, description)
		self.save()
		transaction.save()
	
	def _create_transaction(self, type, amount, description, recipient=None):
		if amount < 0:
			raise Exception("Invalid amount")
		return Transaction(account=self, type=type, 
						   account_to=recipient,
						   amount=amount, 
						   balance=self.balance.amount, 
						   description=description)

	
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
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	balance = models.DecimalField(max_digits=12, decimal_places=2)
	description = models.TextField()
	
	created = models.DateTimeField(auto_now_add=True, editable=False)
