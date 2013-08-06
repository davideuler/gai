from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from gai import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gai.views.home', name='home'),
    # url(r'^gai/', include('gai.foo.urls')),
    url(r'^$', 'gai.views.index'),
    url(r'^([BrAmnHPqRjibCe2ghYMW5XufzUTNxVZvt9EKFdyJ7D8SLa4p6w3QsckG]{2,})$',
        'gai.views.default_redirect'),
    url(r'^a/shorten$', 'gai.views.shorten_url'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^a/admin/', include(admin.site.urls)),
)
