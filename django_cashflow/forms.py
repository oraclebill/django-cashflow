from django import newforms as forms
from money.contrib.django.forms import MoneyField
from money.Money import Money, CURRENCY
from models import *


__all__ = ('AccountForm', 'TransactionForm', 'MoveMoneyForm', 'FilterHistoryForm', )


def get_def_currency():
    from django.conf import settings
    if hasattr(settings, 'CASHFLOW_DEFAULT_CURRENCY'):
        return settings.CASHFLOW_DEFAULT_CURRENCY
    return None

def get_def_money():
    currency = get_def_currency()
    if currency:
        return Money(0, currency)
    return None

def add_empty_label(choices, empty_label=u''):
    a = list(choices)
    a.insert(0, ('', empty_label))
    return tuple(a) 

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ('user',)
    balance = forms.CharField(max_length=42, help_text="Example: USD 100")
    
    def clean_number(self):
        value = self.cleaned_data['number']
        try:
            Account.objects.get(number=value)
            raise forms.ValidationError("This account number alredy exist.") 
        except Account.DoesNotExist:
            return value
    
    def clean_balance(self):
        value = self.cleaned_data['balance']
        try:
            money_val = Money()
            money_val.from_string(value)
            if money_val.currency.code == 'XXX' and get_def_currency():
                money_val.currency = CURRENCY[get_def_currency()]
        except:
            raise forms.ValidationError("Invalid money value")
        return money_val
        
class TransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    tag = forms.IntegerField(widget=forms.Select(choices=add_empty_label(TX_TAG_CHOICES)), required=False)
    description = forms.CharField(widget=forms.Textarea())


class MoveMoneyForm(forms.Form):
    
    def __init__(self, data=None, from_account=None, *arg, **kwarg):
        self.base_fields['account'].queryset = Account.objects\
                            .filter(balance_currency=from_account.balance_currency)\
                            .exclude(number__exact=from_account.number)
        super(MoveMoneyForm, self).__init__(data, *arg, **kwarg)

    account = forms.ModelChoiceField(None)
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    tag = forms.IntegerField(widget=forms.Select(choices=add_empty_label(TX_TAG_CHOICES)), required=False)
    description = forms.CharField(widget=forms.Textarea())


class FilterHistoryForm(forms.Form):
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    keywords = forms.CharField(required=False)
