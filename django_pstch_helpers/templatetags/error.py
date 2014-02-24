"""
#TODO: Add module docstring
"""
from django.template import Library, Node

register = Library() #pylint: disable=C0103

@register.tag
def raise_exception(parser, token):
    """
    #TODO: Add method docstring
    """
    #pylint: disable=W0613
    return RaiseExNode()

class RaiseExNode(Node):
    """
    #TODO: Add method docstring
    """
    def render(self, context):
        raise Exception("Test Exception")
