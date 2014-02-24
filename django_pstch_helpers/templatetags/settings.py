"""
#TODO: Add module docstring
"""
#TODO: Find out why pylint is not working on this file
from django.template import Library, Node, TemplateSyntaxError
from django.conf import settings

register = Library() #pylint: disable=C0103

@register.tag
def setting(parser, token):
    """
    #TODO: Add method docstring
    """
    #pylint: disable=W0613
    try:
        option = token.split_contents()[1]
    except ValueError:
        raise TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents[0])
    return SettingNode(option)

class SettingNode(Node):
    """
    #TODO: Add class docstring
    """
    def __init__(self, option):
        """
        #TODO: Add method docstring
        """
        self.option = option
    def render(self, context):
        """
        #TODO: Add method docstring
        """
        context[self.option] = getattr(settings, self.option)
        return ""
