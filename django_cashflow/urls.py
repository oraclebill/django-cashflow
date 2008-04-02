from django.conf.urls.defaults import *

urlpatterns = patterns('django_cashflow.views',
    url(r'^$', 'list_accounts', name="list-accounts"),
    url(r'^account/view/(?P<number>.*)/$', 'account_details', name="account-details"),
    url(r'^account/add/$', 'add_account', name="add-account"),
    url(r'^operation/add/(?P<number>.*)/$', 'add_money', name="cashflow-add-money"),
    url(r'^operation/withdraw/(?P<number>.*)/$', 'withdraw_money', name="cashflow-withdraw-money"),
    url(r'^operation/move/(?P<number>.*)/$', 'move_money', name="cashflow-move-money"),
    url(r'^history/(?P<number>.*)/$', 'history', name="cashflow-history"),
)
