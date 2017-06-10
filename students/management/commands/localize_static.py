import os
import urllib2

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from django.conf import settings

class Command(BaseCommand):
    help = _(u'Downloads external css and javascript files to folder static')

    def handle(self, *args, **options):
        base_file = open(os.path.join(settings.BASE_DIR, 'students/templates/students/base.html'), 'r')
        text_file = base_file.readlines()
        base_file.close()
        n = 0
        for text_line in text_file:
            if 'https://' or 'http://' in text_line:
                href = text_line[text_line.find('"')+1:text_line.find('"', text_line.find('"')+1)]
                if href.find('css/') > 0:
                    online_href = urllib2.urlopen(href).read()
                    new_file_name = href[href.find('css/')+4:href.find('.', href.find('css/')+1)] + '.css'
                    new_file = open(os.path.join(settings.BASE_DIR, 'students/static/css', new_file_name), 'w')
                    new_file.write(online_href)
                    new_file.close()
                    new_href = "{{ PORTAL_URL }}{% static 'css/" + new_file_name + "' %}"
                    new_text_line = text_line.replace(text_line[text_line.find('"')+1:text_line.find('"', text_line.find('"')+1)], new_href)
                    text_file[n] = new_text_line
                elif href.find('.js') > 0:
                    online_href = urllib2.urlopen(href).read()
                    new_file_name = href[href.rfind('/')+1:href.rfind('.')]
                    new_file_name = new_file_name.replace('.', '_') + '.js'
                    new_file = open(os.path.join(settings.BASE_DIR, 'students/static/js', new_file_name), 'w')
                    new_file.write(online_href)
                    new_file.close()
                    new_href = "{{ PORTAL_URL }}{% static 'js/" + new_file_name + "' %}"
                    new_text_line = text_line.replace(text_line[text_line.find('"')+1:text_line.find('"', text_line.find('"')+1)], new_href)
                    text_file[n] = new_text_line
            n += 1
        base_file = open(os.path.join(settings.BASE_DIR, 'students/templates/students/base.html'), 'w')
        base_file.writelines(text_file)
        base_file.close()
                    
                
