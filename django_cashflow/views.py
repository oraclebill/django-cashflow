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
def account_details(request, id):
    account = get_object_or_404(Account, id=id, user=request.user)
    return locals()
