from django import newforms as forms
from models import *

__all__ = ('AccountForm',)


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ('user',)
    balance = forms.DecimalField(initial="0.00")