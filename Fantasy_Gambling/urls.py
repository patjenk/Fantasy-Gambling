from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = 'Fantasy_Gambling.bets.views.custom_404'

urlpatterns = patterns('',
    # Example:
    # (r'^Fantasy_Gambling/', include('Fantasy_Gambling.foo.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),

    (r'^admin/', include(admin.site.urls)),
    (r'^joinleague/', 'Fantasy_Gambling.bets.views.joinleague'),
    (r'^logout/', 'Fantasy_Gambling.bets.views.logout_view'),
    (r'^login/', 'Fantasy_Gambling.bets.views.index'),
    (r'^user/(?P<username>\w+)/$', 'Fantasy_Gambling.bets.views.user_profile'),
    (r'.*', 'Fantasy_Gambling.bets.views.index'),
)
