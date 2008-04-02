from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth import views as auth_views 

urlpatterns = patterns('',
    (r'^', include('django_cashflow.urls')),
#    (r'^admin/', include('django.contrib.admin.urls')),
    
    #Accounts stuff -------------------------------------------------
    url(r'^accounts/login/$', auth_views.login, name='auth_login'),
    url(r'^accounts/logout/$',auth_views.logout, name='auth_logout'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )