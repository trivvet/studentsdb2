from django import template

register = template.Library()

# Usage: {% pagenav students is_paginated paginator %}

@register.tag
def pagenav(parser, token):
    # parse tag arguments
    try:
        # split_contents knows how to split quoted strings
        tag_name, object_list, is_paginated, paginator = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires 3 arguments" % token.contents.split()[0])

    # create PageNavNode object passing tag arguments
    return PageNavNode(object_list, is_paginated, paginator)

class PageNavNode(template.Node):

    def __init__(self, object_list, is_paginated, paginator):
        self.object_list = template.Variable(object_list)
        self.is_paginated = template.Variable(is_paginated)
        self.paginator = template.Variable(paginator)

    def render(self, context):
        t = template.loader.get_template('students/pagination.html')
        return t.render(template.Context({
            'page_obj': self.object_list.resolve(context),
            'is_paginated': self.is_paginated.resolve(context),
            'paginator': self.paginator.resolve(context)},
        ))
