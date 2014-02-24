"""
#TODO: Add module docstring
"""
#pylint: disable=W0142
def get_filter_class(filter_model, filter_class):
    """
    #TODO: Add method docstring
    """
    class FilterSet(filter_class):
        #pylint: disable=W0232, R0903
        """
        #TODO: Add class docstring
        """
        lookup_type = None
        class Meta(filter_class.Meta):
            """
            #TODO: Add class docstring
            """
            model = filter_model
    return FilterSet

def make_url_name(namespaces, object_url_name, action):
    """
    Joins namespaces with an action and optionally an URL name

    Will return "<namespaces>:<object_url_name>-<action>" if
    object_url_name is not None, otherwise "<namespaces>:<action>"
    (without the '<>').
    """
    def _namespaces():
        return ":".join(namespaces if namespaces else [])
    def _short_url_name():
        return "-".join([object_url_name, action] if object_url_name else [action])
    if namespaces:
        return  ":".join([
            _namespaces(),
            _short_url_name()
        ])
    else:
        return ":".join([
            _short_url_name()
        ])

def contribute_viewset_to_views(views, viewset):
    """
    Adds the view 3-tuple returned by the viewset to another dict
    ('views'). If a tuple is already present in views[viewset.action],
    set the value as list with the two items, and if it's a list, just
    append the tuple.

    Note: this function does not return any value, as it works
    directly on the dict given as first argument.
    """
    # TODO: Write test for this class, testing the three behaviours :
    #  - no current item
    #  - current item is list
    #  - current is singleton
    # get action name
    action = viewset.action

    # get new view tuple
    new = viewset.get_tuple()
    # get old dict value
    current = views.get(action)

    if current:
        # current not None
        if isinstance(current, list):
            # list, append
            views[action].append(new)
        else:
            # singleton, create list
            views[action] = [current,
                             new]
    else:
        # current is None, set new value
        views[action] = new

def get_model_view_args(action, view, model):
    # TODO: Write test
    """
    compiles the list of view arguments using model.get_view_args()
    for the given model (or for each model if it is a list). if
    get_view_args() returns a callable, or a dict with callables as
    values, they will be evaluated with 3 arguments : action ; view ;
    item

    WARNING: if the same keys are present in get_view_args() for
    multiple models, the last evaluated value will be used
    """
    args = {}
    if model and not hasattr(model, '__iter__'):
        # singleton, make a list
            models = [model, ]
    else:
        models = model

    for _model in models:
        # for each view arguments dictionary
        _args = _model.get_view_args().get(action)
        if callable(_args):
            # call the callable
            _args = _args(action, view, _model)
        if _args is None:
            # we want {} instead of None
            _args = {}
        else:
            # wasn't None, just check for callables in the values
            for key in _args:
                if callable(_args[key]):
                    # call the callable
                    _args[key] = _args[key](action, view, _model)

        # merge _args into args
        args = dict(args,
                    **_args)

    return args
