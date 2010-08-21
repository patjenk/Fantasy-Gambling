from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^Fantasy_Gambling/', include('Fantasy_Gambling.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^user/(?P<user_name>\w+)/$', 'Fantasy_Gambling.bets.views.user_profile'),
    (r'^admin/', include(admin.site.urls)),
    (r'.*', 'Fantasy_Gambling.bets.views.index'),
    
)
