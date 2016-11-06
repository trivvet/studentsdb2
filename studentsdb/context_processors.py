# from .settings import PORTAL_URL

def students_proc(request):
#    import pdb;pdb.set_trace()
    PORTAL_URL = request.META['wsgi.url_scheme'] +'://' + request.META['HTTP_HOST']
    return {'PORTAL_URL': PORTAL_URL}
