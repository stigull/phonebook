#coding: utf-8
from django.db import connection, backend, models
from django.contrib.auth.models import User

import user_profile
from user_profile.settings import controller

PROFILE_MODEL = controller.get_profile_model()

def create_search_view(sender, app, created_models, verbosity, interactive, **kwargs):
    VIEW_SQL = """
                CREATE OR REPLACE VIEW phonebook_usersearchview
                    (profile_id,
                        username,
                        kennitala,
                        fullname,
                        fullname_sans_middlename,
                        first_name,
                        middlenames,
                        last_name,
                        address,
                        phone,
                        gsm)
                AS
                    SELECT
                        p.id as profile_id,
                        u.username as username,
                        p.kennitala as kennitala,
                        u.first_name || ' ' || p.middlenames || ' ' || u.last_name as fullname,
                        u.first_name || ' ' || u.last_name as fullname_sans_middlename,
                        u.first_name as first_name,
                        p.middlenames as middlenames,
                        u.last_name as last_name,
                        p.address as address,
                        p.phone as phone,
                        p.gsm as gsm
                    FROM
                        %(user_table_name)s as u,
                        %(profile_table_name)s as p
                    WHERE
                        u.id = p.user_id
                    ORDER BY fullname
                """ % {'user_table_name': User._meta.db_table,
                        'profile_table_name': PROFILE_MODEL._meta.db_table }

    cursor = connection.cursor()
    cursor.execute(VIEW_SQL)
    cursor.close()


models.signals.post_syncdb.connect(create_search_view, sender = user_profile.models)
