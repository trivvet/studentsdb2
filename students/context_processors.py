from .util import get_groups

def groups_processor(request):
    return {'groups_all': get_groups(request)}
