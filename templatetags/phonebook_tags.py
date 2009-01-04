#coding: utf-8
import random

from django import template
from django.contrib.auth.models import User

from user_profile.settings import controller
from phonebook.forms import UserSearchForm

register = template.Library()

profile_model = controller.get_profile_model()
 
 
def phonebook_search_form(query = ""):
    form = UserSearchForm(auto_id = "search-form-%s", initial = {'query': query })
    form.id = "search-form"
    return {'form' : form , 'dict': form.__dict__}
register.inclusion_tag('phonebook/forms/search_form.html')(phonebook_search_form)

def get_random_user():
    """
    Usage:  {% get_random_user %}
    After:  A random user has been selected from the database and displayed
    """
    user = User.objects.all()[random.randrange(0, User.objects.count())]
    return {'profile': user.get_profile() }
register.inclusion_tag('phonebook/snippets/random_user.html')(get_random_user)
    

def get_list_of_users(parser, token):
    """
    Usage:  {% get_list_of_objects as varname %}
    After:  varname contains a list of all the User objects
    """
    bits = token.contents.split()
    #bits = ['get_list_of_objects', 'as', varname ]
    if len(bits) != 3:
        raise template.TemplateSyntaxError("%s tag takes one arguments" % bits[0])
    
    if bits[1] != 'as':
        raise template.TemplateSyntaxError("Second argument for %s must be 'as'" % bits[0])

    return GetListOfUsersNode(bits[2])
register.tag('get_list_of_users', get_list_of_users)

class GetListOfUsersNode(template.Node):
    def __init__(self, varname):
        
        self.varname = varname
        self.users = profile_model.objects.select_related().all()
        
    def render(self, context):
        context[self.varname] = self.users
        return ''

    
