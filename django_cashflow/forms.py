from django import newforms as forms
from models import *

__all__ = ('AccountForm', 'TransactionForm',)


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ('user',)
        
class TransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    description = forms.CharField(widget=forms.Textarea())