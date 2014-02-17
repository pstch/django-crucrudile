_PK_ARG = "(?P<pk>\d+)"

class ViewSet():
    action = ""
    url  = ""
    view = ""
    extra_args = {}
    def get_tuple(self):
        return (url, view, extra_args)

