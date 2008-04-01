from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views 

urlpatterns = patterns('',
    (r'^', include('django_cashflow.urls')),
#    (r'^admin/', include('django.contrib.admin.urls')),
    
    #Accounts stuff -------------------------------------------------
    url(r'^accounts/login/$', auth_views.login, name='auth_login'),
    url(r'^accounts/logout/$',auth_views.logout, name='auth_logout'),
)
