from django.conf.urls.defaults import *

from phonebook.views import search

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', kwargs = {'template': 'phonebook/phonebook_base.html'}, name = 'phonebook'),
    url(r'^leit/$', search, name = 'phonebook_search'),


) 
