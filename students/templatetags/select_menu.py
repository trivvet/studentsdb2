from django import template

register = template.Library()

# Usage: {% pagenav students is_paginated paginator %}

@register.tag
def select_menu(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, path, current_url = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires 2 arguments" % token.contents.split()[0]
        )

    return SelectMenuNode(path, current_url)
    
class SelectMenuNode(template.Node):
    def __init__(self, path, current_url):
        self.path = template.Variable(path)
        self.current_url = template.Variable(current_url)
        
    def render(self, context):
        if self.path.resolve(context) == self.current_url.resolve(context):
            return 'class="active"'
        else:
            return ''
