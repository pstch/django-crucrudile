"""
#TODO: Add module docstring
"""
_PK_ARG = r"(?P<pk>\d+)"

class ViewSet(object):
    """
    #TODO: Add class docstring
    """
    #pylint: disable=R0903, W0232
    action = ""
    url = ""
    view = ""
    extra_args = {}
    def get_tuple(self):
        """
        #TODO: Add method docstring
        """
        return (self.url, self.view, self.extra_args)

