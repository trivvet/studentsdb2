from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate(objects, size, request, context, var_name='object-list'):

    '''Paginate objects provided by view/

    This function takes:
      * list of elements;
      * number of objects per page;
      * request object to get url parameters from;
      * context to set new variables info;
      * var_name - variable name for list of objects

    It returns updated context object/
    '''

    # apply pagination
    paginator = Paginator(objects, size)

    # try to get page number from request
    page = request.GET.get('page', '1')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999),
        # deliver last page of result
        object_list = paginator.page(paginator.num_pages)

    # set variables into context
    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator

    return context

def paginate_hand(objects, size, request, context, var_name='object-list'):


    try:
        l = objects.count()
    except:
        l = len(objects)
    
    if l > 0:
        number = size
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        num_pages = l / number
        if l % number > 0:
            num_pages += 1
        # block for student_list template
        if num_pages > 1:
            page_range = []
            for i in range(1, num_pages+1):
                page_range.append(i)
            context['addition'] = {
                'has_other_pages': True,
                'page_range': page_range}
        else:
            context['addition'] = {}
    
        if page > 0 and page < num_pages:
            context[var_name] = objects[number*(page-1):number*page]
            context['addition']['page'] = page
        else:
            context[var_name] = objects[number*(num_pages-1):l]
            context['addition']['page'] = num_pages

        context['addition']['counter'] = number * (context['addition']['page'] - 1)
    else:
        context = {}
    # end handmade paginator
    return context

def get_groups(request):
    """Returns list of existing groups"""
    # deferred import of Group model to avoid cycled imports
    from .models import Group

    # get currently selected group
    cur_group = get_current_group(request)

    groups = []
    for group in Group.objects.all().order_by('title'):
        groups.append({
          'id': group.id,
          'title': group.title,
          'leader': group.leader and (u'%s %s' % (group.leader.first_name,
                    group.leader.last_name)) or None,
          'selected': cur_group and cur_group.id == group.id and True or False
        })

    return groups

def get_current_group(request):

    """Returns currently selected group or None"""

    # we remember selected group in a cookie
    pk = request.COOKIES.get('current_group')

    if pk:
        from .models import Group
        try:
            group = Group.objects.get(pk=int(pk))
        except Group.DoesNotExist:
            return None
        else:
            return group

    else:
        return None
