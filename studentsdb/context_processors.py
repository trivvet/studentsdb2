# from .settings import PORTAL_URL
import pytz
from django.utils import timezone

def students_proc(request):
    #import pdb;pdb.set_trace()
    # this check is required for test_student_views
    try:
        request.META['HTTP_HOST']
    except KeyError:
        http_host = request.META['REMOTE_ADDR'] + request.META['SERVER_PORT']
    else:
        http_host = request.META['HTTP_HOST']
    PORTAL_URL = request.META['wsgi.url_scheme'] +'://' + http_host
    time = timezone.now()
    return {'PORTAL_URL': PORTAL_URL, 'time': time}
