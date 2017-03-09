from django import template

register = template.Library()

# Usage: {% pagenav students is_paginated paginator %}

@register.inclusion_tag('students/pagination.html')
def pagenav(page_obj, is_paginated, paginator):
    # Display page navigation for given list of objects
    return {
        'page_obj': page_obj,
        'is_paginated': is_paginated,
        'paginator': paginator
    }
