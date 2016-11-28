"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views import static

from students.views import students, groups, journal, exams, results
from students.views.students import StudentUpdateView

from .settings import MEDIA_ROOT, DEBUG

urlpatterns = [
  
    #Students urls
    url(r'^$', students.students_list, name='home'),
    url(r'^students/add/$', students.students_add, name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit', StudentUpdateView.as_view(),
#        students.students_edit, 
        name='students_edit'),
    url(r'^students/(?P<sid>\d+)/delete', students.students_delete,
        name='students_delete'),
  
    #Groups urls
    url(r'^groups/$', groups.groups_list, name='groups'),
    url(r'^groups/add/$', groups.groups_add, name='groups_add'),
    url(r'^groups/(?P<gid>\d+)/edit', groups.groups_edit, 
        name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete', groups.groups_delete,
        name='groups_delete'),
  
    # Journal url  
    url(r'^journal/$', journal.journal_list, name='journal'),

    # Exams urls
    url(r'^exams/$', exams.exams_list, name='exams'),
    url(r'^exams/add/$', exams.exams_add, name='exams_add'),
    url(r'^exams/(?P<eid>\d+)/edit', exams.exams_edit, 
        name='exams_edit'),
    url(r'^exams/(?P<eid>\d+)/delete', exams.exams_delete,
        name='exams_delete'),
        
    # Results urls
    url(r'^results/$', results.results_list, name='results'),
    url(r'^results/add/$', results.results_add, name='results_add'),
    url(r'^results/(?P<rid>\d+)/edit', results.results_edit, 
        name='results_edit'),
    url(r'^results/(?P<rid>\d+)/delete', results.results_delete,
        name='results_delete'),
    
    url(r'^admin/', admin.site.urls),
]

if DEBUG:
    # serve files from media folder
    # import pdb;pdb.set_trace()
    urlpatterns.append(url(r'^media/(?P<path>.*)$', static.serve, 
        {'document_root': MEDIA_ROOT}))
