# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# View for Journal

def journal_list(request):
    return HttpResponse('<h1>Journal List</h1>')


# Create your views here.
