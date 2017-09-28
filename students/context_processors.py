from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError

from .util import get_groups
from ipware.ip import get_ip

def groups_processor(request):
    return {'groups_all': get_groups(request)}

def get_user_info(request):
    g = GeoIP2()
    user_ip = get_ip(request)
    
    try:
        user_city = g.city(user_ip)
    except AddressNotFoundError:
        user_city = None
    try:
        user_country = g.country(user_ip)
    except AddressNotFoundError:
        user_country = None
    return {'user_city': user_city, 'user_country': user_country, 'user_ip': user_ip}
