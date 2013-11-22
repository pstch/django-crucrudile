from django import template
from django.conf import settings
register = template.Library()

@register.tag
def setting (parser, token): 
    try:
        tag_name, option = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents[0]
    return SettingNode(option)

class SettingNode (template.Node): 
    def __init__ (self, option): 
        self.option = option
    def render (self, context): 
        context[self.option] = getattr(settings,self.option)

