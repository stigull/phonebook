#coding: utf-8
 
from django.db import models
from django.db.models import Q

from user_profile.settings import controller

ProfileModel = controller.get_profile_model()

class UserSearchViewManager(models.Manager):
    
    def search(self, query):
        return super(UserSearchViewManager, self).get_query_set().filter(
                                    Q(username__icontains = query) |
                                    Q(fullname__icontains = query) | 
                                    Q(fullname_sans_middlename__icontains = query) | 
                                    Q(first_name__icontains = query) | 
                                    Q(middlenames__icontains = query) |
                                    Q(last_name__icontains = query) | 
                                    Q(address__icontains = query) |
                                    Q(phone__icontains = query) |
                                    Q(gsm__icontains = query)).select_related().order_by("fullname")[:5]


class UserSearchView(models.Model):
    profile = models.ForeignKey(ProfileModel, primary_key = True)
    username = models.CharField(max_length = 30)
    kennitala = models.CharField(max_length = 11)
    fullname = models.CharField(max_length = 600)
    fullname_sans_middlename = models.CharField(max_length = 600)
    first_name = models.CharField(max_length = 600)
    middlenames = models.CharField(max_length = 600)
    last_name = models.CharField(max_length = 600)
    address = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 7)
    gsm = models.CharField(max_length = 7)
    
    objects = UserSearchViewManager()
    
    class Meta:
        db_table = "phonebook_usersearchview"

    
    
