# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# View for Journal

def journal_list(request):
    students = (
        {'id': 1,
         'first_name': u'Вадим',
         'last_name': u'Афанасьєв',
         'ticket': 22,
         'image': 'img/1.jpeg'},
         {'id': 2,
         'first_name': u'Олег',
         'last_name': u'Обліховський',
         'ticket': 108,
         'image': 'img/2.jpeg'},
         {'id': 3,
         'first_name': u'Анна',
         'last_name': u'Григоренко',
         'ticket': 67,
         'image': 'img/3.jpeg'}
    )
    groups = (
         {'id': 1,
          'name': u'БМ - 1',
          'leader': {'first_name': u'Андрій', 'last_name': u'Комисливий', 
                    'id': 4}},
         {'id': 2,
          'name': u'БМ - 2',
          'leader': {'first_name': u'Павло', 'last_name': u'Очерет', 
                    'id': 5}},
         {'id': 3,
          'name': u'БМ - 3',
          'leader': {'first_name': u'Олена', 'last_name': u'Доровська', 
                    'id': 6}},
    )
    days = []
    day_names = [u'Пн', u'Вт', u'Ср', u'Чт', u'Пт', u'Сб', u'Нд']
    for i in range(1, 31):
      days.append(day_names[i%7-1])
    print days
#   import pdb;pdb.set_trace()
    return render(request, 'students/journal.html', 
        {'students': students, 'groups': groups, 'days': days, 
         'day_names': day_names})


# Create your views here.
