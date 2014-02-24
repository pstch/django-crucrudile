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
    return  ":".join(
        ":".join(namespaces),
        "-".join[object_url_name, action] if object_url_name else action
    )

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
            views[action].append(current)
        else:
            # singleton, create list
            views[action] = [current,
                             new]
    else:
        # current is None, set new value
        views[action] = new

def mix_intersection(first, second):
    """
    #TODO: Add method docstring
    """
    # NOTE: should not be needed anymore now that we switched
    # to ViewSets and contribute_viewset_to_views
    # puke before reading for best experience
    # TODO: Write test for this function (by comparing dicts)
    if first and second and set(first) & set(second):
        for intersection in list(set(first) & set(second)):
            if isinstance(first[intersection], (list)) and \
               isinstance(second[intersection], (list)):
                first[intersection] += second[intersection]
            elif isinstance(first[intersection], (list)):
                first[intersection].append(second[intersection])
            elif isinstance(second[intersection], (list)):
                second[intersection].append(first[intersection])
                first[intersection] = second[intersection]
            else:
                first[intersection] = [first[intersection],
                                       second[intersection]]
            second.pop(intersection)
    return first, second

def mix_views(*args):
    """
    #TODO: Add method docstring
    """
    # NOTE: should not be needed anymore now that we switched
    # to ViewSets and contribute_viewset_to_views
    args = list(args)
    if not args:
        return {}
    if len(args) is 1:
        return args[0].copy()
    elif len(args) > 1:
        current, remaining = mix_intersection(
            args[0].copy(),
            mix_views(*args[1:])
        )

        return dict(current,
                    **remaining)

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
    if not hasattr(model, '__iter__'):
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
