from django.db import models
from django.db.transaction import commit_on_success
from django.contrib.auth.models import User
from money.contrib.django.models.fields import MoneyField

__all__ = ('Account', 'Transaction',
		   'TX_ADD', 'TX_WITHDRAW', 'TX_MOVE',
		   'TX_CHOICES')

#TODO: declare exceptions

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
		if (self.balance.amount - amount) < 0:
			raise Exception("Withdraw amount couldn't be more than account balance")
		self.balance -= amount
		transaction = self._create_transaction(TX_WITHDRAW, amount, description)
		self.save()
		transaction.save()
	
	@commit_on_success
	def move_money(self, to_account, amount, description):
		if (self.balance.amount - amount) < 0:
			raise Exception("Withdraw amount couldn't be more than account balance")
		if self.balance.currency != to_account.balance.currency:
			raise Exception("Different currencies")
		#TODO: does need to check self.user and to_account.user is the same ?
		self.balance -= amount
		to_account.balance += amount
		transaction = self._create_transaction(TX_MOVE, amount, description, to_account)
		self.save()
		to_account.save()
		transaction.save()
	
	def _create_transaction(self, type, amount, description, recipient=None):
		if amount < 0:
			raise Exception("Invalid amount")
		recipient_balance = None
		if recipient:
			recipient_balance = recipient.balance.amount
		return Transaction(account=self, type=type, 
						   recipient_account=recipient,
						   amount=amount, 
						   balance=self.balance.amount, 
						   recipient_balance=recipient_balance,
						   description=description)
	
	def __unicode__(self):
		return self.number

	
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
	recipient_account = models.ForeignKey(Account, blank=True, null=True, related_name='move_transactions')
	type = models.SmallIntegerField(choices=TX_CHOICES)
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	balance = models.DecimalField(max_digits=12, decimal_places=2)
	recipient_balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
	description = models.TextField()
	
	created = models.DateTimeField(auto_now_add=True, editable=False)
