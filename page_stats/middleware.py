# -*- coding: utf-8 -*-

import time
from datetime import datetime
from operator import add

from django.db import connection
from django.http import HttpResponse

from studentsdb import settings

class RequestDatabaseTimeMiddleware(object):
    '''Display full request time on a page'''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # get number of db queries
        n = len(connection.queries)

        # time the view
        response = self.get_response(request)

        if settings.DEBUG == False:
            return response

        # compute the db time for the queries just run
        db_queries = len(connection.queries) - n
        if db_queries:
            db_time = reduce(add, [float(q['time']) for q in connection.queries[n:]])
        else:
            db_time = 0.0
        
        if 'text/html' in response.get('Content-Type', ''):
            response.content = response.content.replace('<p id="response-time-db">', '<p class="bg-info">Database found took %s' % str(db_time))
        
        return response


class RequestTimeMiddleware(object):
    '''Display request time on a page'''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = datetime.now()

        response = self.get_response(request)

        if settings.DEBUG == False:
            return response

        end_time = datetime.now()
        time_response = end_time - start_time
    
        if time_response.seconds > 1:
            return HttpResponse(u'<h2>Обробка запиту надто повільна. Розробник - переглянь свій код</h2>')
        
        if 'text/html' in response.get('Content-Type', ''):
            response.content = response.content.replace('<p id="response-time">', '<p class="bg-info">Request took %s' % str(time_response))
        
        return response

    def process_view(self, request, view, args, kwargs):
         return None

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return HttpResponse('Exception found %s:' % exception)
