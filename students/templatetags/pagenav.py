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

#@register.tag
#def pagenav(parser, token):
    ## This version uses a regular expression to parse tag contents.
    #try:
        ## Splitting by None == splitting by spaces.
        #tag_name, page_obj, is_paginated, paginator = token.contents.split()
    #except ValueError:
        #raise template.TemplateSyntaxError(
            #"%r tag requires 3 arguments" % token.contents.split()[0]
        #)

    #return PagenavNode(page_obj, is_paginated, paginator)
    
#class PagenavNode(template.Node):
    #def __init__(self, page_obj, is_paginated, paginator):
        #self.page_obj = template.Variable(page_obj)
        #self.is_paginated = template.Variable(is_paginated)
        #self.paginator = template.Variable(paginator)
        
    #def render(self, context):
        #t = context.template.engine.get_template('students/pagination.html')
        #context['navigation'] = t.render(template.Context({
            #'page_obj': self.page_obj.resolve(context),
            #'is_paginated': self.is_paginated.resolve(context),
            #'paginator': self.paginator.resolve(context)}
        #))
        #return ''

