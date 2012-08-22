import os
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

'''
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scrubmyaddress.views.home', name='home'),
    # url(r'^scrubmyaddress/', include('scrubmyaddress.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
'''

urlpatterns = patterns('addrinfo.views', 
                       url(r'^$', 'addr_std'),
                       url(r'^addr_city_state/$', 'city_state_lookup'),
                       url(r'^addr_zip_code/$', 'zip_code_lookup'),
                       )

urlpatterns += patterns(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        #{'document_root': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media')}),
                        {'document_root': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media')})


