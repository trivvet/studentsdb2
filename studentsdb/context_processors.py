# from .settings import PORTAL_URL
import pytz
from django.utils import timezone

def students_proc(request):
#    import pdb;pdb.set_trace()
    PORTAL_URL = request.META['wsgi.url_scheme'] +'://' + request.META['HTTP_HOST']
    time = timezone.now()
    return {'PORTAL_URL': PORTAL_URL, 'time': time}
