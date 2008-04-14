from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import *
from forms import *


#Utils --------------------------------------------------

def render_to_response(request, template_name, context_dict = {}):
    from django.template import RequestContext
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict)
    return _render_to_response(template_name, context_instance=context)


def render_to(template_name):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if not isinstance(output, dict):
                return output
            return render_to_response(request, template_name, output)
        return wrapper
    return renderer


#Views --------------------------------------------------


@login_required
@render_to('cashflow/accounts.html')
def list_accounts(request):
    accounts = request.user.account_set.all()
    return locals()


@login_required
@render_to('cashflow/account_form.html')
def add_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.user = request.user
            new_acc.save()
            return HttpResponseRedirect(reverse("list-accounts"))
    else:
        form = AccountForm()
    return locals()

@login_required
@render_to('cashflow/account_details.html')
def account_details(request, number):
    account = get_object_or_404(Account, number=number, user=request.user)
    return locals()


def _simple_transaction_request(request, account, proc_method):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            proc_method(amount=form.cleaned_data['amount'],
                        tag=form.cleaned_data['tag'],
                        description=form.cleaned_data['description'])
            return HttpResponseRedirect(reverse("account-details", args=[account.number]))
    else:
        form = TransactionForm()
    return locals()


@login_required
@render_to('cashflow/add_money.html')
def add_money(request, number):
    account = get_object_or_404(Account, number=number, user=request.user)
    return _simple_transaction_request(request, account, account.add_money)


@login_required
@render_to('cashflow/withdraw_money.html')
def withdraw_money(request, number):
    account = get_object_or_404(Account, number=number, user=request.user)
    return _simple_transaction_request(request, account, account.withdraw_money)


@login_required
@render_to('cashflow/move_money.html')
def move_money(request, number):
    account = get_object_or_404(Account, number=number, user=request.user)
    if request.method == 'POST':
        form = MoveMoneyForm(request.POST, from_account=account)
        if form.is_valid():
            account.move_money(to_account=form.cleaned_data['account'],
                               amount=form.cleaned_data['amount'],
                               tag=form.cleaned_data['tag'],
                               description=form.cleaned_data['description'])
            return HttpResponseRedirect(reverse("account-details", args=[account.number]))
    else:
        form = MoveMoneyForm(from_account=account)
    return {'form':form}


@login_required
@render_to('cashflow/history.html')
def history(request, number):
    account = get_object_or_404(Account, number=number, user=request.user)
    from django.db.models import Q
    queryset = Transaction.objects.filter(
            Q(account=account) | Q(recipient_account=account)).order_by('-created')
    
    if request.method == 'POST':
        form = FilterHistoryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['date_from']:
                queryset = queryset.filter(created__gte=form.cleaned_data['date_from'])
            if form.cleaned_data['date_to']:
                queryset = queryset.filter(created__lte=form.cleaned_data['date_to'])
            if form.cleaned_data['keywords']:
                 queryset = queryset.filter(description__contains=form.cleaned_data['keywords'])
    else:
         form = FilterHistoryForm()
    
    history_items = []
    for t in queryset:
        item = {'description':t.description, 'datetime':t.created, 'tag': t.tag,
                'debit':'', 'credit':'', 'correspondent':''}
        if t.type == TX_ADD:
            item['credit'] = t.amount
            item['balance'] = t.balance
            item['balance_before'] = t.balance - t.amount
        elif t.type == TX_WITHDRAW:
            item['debit'] = t.amount
            item['balance'] = t.balance
            item['balance_before'] = t.balance + t.amount
        elif t.type == TX_MOVE:
            if t.account == account:
                item['debit'] = t.amount
                item['balance'] = t.balance
                item['correspondent'] = t.recipient_account
                item['balance_before'] = t.balance + t.amount
            else:
                item['credit'] = t.amount
                item['balance'] = t.recipient_balance
                item['correspondent'] = t.account
                item['balance_before'] = t.recipient_balance - t.amount
        history_items.append(item)
        
    return {'history':history_items, 'form':form}
    
