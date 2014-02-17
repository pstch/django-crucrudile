def make_url_name(namespaces, object_url_name, action):
    """
    Joins namespaces with an action and optionally an URL name

    Will return "<namespaces>:<object_url_name>-<action>" if object_url_name is not None, otherwise "<namespaces>:<action>" (without the '<>').
    """
    return  ":".join(":".join(namespaces),
                     "-".join[object_url_name, action] if object_url_name else action)

def contribute_viewset_to_views(views, viewset):
    """
    Adds the view 3-tuple returned by the viewset to another dict ('views'). If a tuple is already present in views[viewset.action], set the value as list with the two items, and if it's a list, just append the tuple.

    Note: this function does not return any value, as it works directly on the dict given as first argument.
    """
    # get action name
    action = viewset.action

    # get new view tuple
    new = viewset.get_tuple()
    # get old dict value
    current = views.get(action)

    if current:
        # current not None
        if isinstance(current, (list)):
            # list, append
            views[action].append()
        else:
            # singleton, create list
            views[action] = list(current,
                                 new)
    else:
        # current is None, set new value
        views[action] = new

def mix_intersection(first, second):
    # puke before reading for best experience
    if first and second and set(first) & set(second):
        for intersection in list(set(first) & set(second)):
            if isinstance(first[intersection],(list)) and isinstance(second[intersection], (list)):
                first[intersection] += second[intersection]
            elif isinstance(first[intersection],(list)):
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
    args = list(args)
    if not args:
        return {}
    if len(args) is 1:
        return args[0].copy()
    elif len(args) > 1 :
        current, remaining = mix_intersection(args[0].copy(),
                                           mix_views(*args[1:]))

        return dict(current,
                    **remaining)

def get_model_view_args(action, view, model):
    args = {}
    if not hasattr(model, '__iter__'):
        model = [model, ]
    for item in model:
        if hasattr(item,'URL_VIEW_ARGS'):
            _args = item.URL_VIEW_ARGS.get(action)
            if callable(_args):
                _args = _args(action, view, item)
            if _args is None:
                _args = {}
            args = dict(args,
			**_args)

    return args
