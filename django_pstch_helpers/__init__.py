def get_model_view_args(action, model):
    args = {}
    if hasattr(model, '__iter__'):
        for item in model:
            if hasattr(item,'URL_VIEW_ARGS') and item.URL_VIEW_ARGS.get(action):
                    args = dict(args, **item.URL_VIEW_ARGS.get(action))
    else:
        if hasattr(model,'URL_VIEW_ARGS') and model.URL_VIEW_ARGS.get(action):
            args = model.URL_VIEW_ARGS.get(action)
    return args

