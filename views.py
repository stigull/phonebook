#coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from phonebook.forms import UserSearchForm
from phonebook.db_views import UserSearchView

from user_profile.settings import controller
from utils.djangoutils import JSONResponse

def search(request):
    context = {}

    if request.method == 'GET':
        form = UserSearchForm(data = request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            results = UserSearchView.objects.search(query)

            context['results'] = results
            context['query'] = query
            nr_of_results = results.count()
            if request.is_ajax():
                jsonobject = {  'has_results': nr_of_results != 0,
                                'results': render_to_string('phonebook/snippets/search_results_list_min.html', {'results': results, 'user': request.user }),
                                'nr_of_results': nr_of_results }

                return JSONResponse(object = jsonobject)
            else:
                return render_to_response('phonebook/search_results.html', context , context_instance = RequestContext(request))
    return HttpResponseRedirect(reverse('index'))
