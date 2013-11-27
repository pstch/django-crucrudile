def mix_intersection(first, second):
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

def get_model_args(action, view, model):
    args = {}
    if not hasattr(model, '__iter__'):
        model = [model, ]
    for item in model:
        if hasattr(item,'URL_VIEW_ARGS'):
            _args = item.URL_VIEW_ARGS.get(action)
            if callable(_args):
                _args = _args(action, view, model)
            args = dict(args, _args)

    return args

