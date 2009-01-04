#coding: utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

class UserSearchForm(forms.Form):
    query = forms.CharField(label = _(u"Leita í símaskrá"), min_length = 2, max_length = 400)
    
