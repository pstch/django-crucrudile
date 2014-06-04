def provides(viewset,
             view_class,
             action,
             view_args,
             url_args=None):
    viewset[action] = ViewDefinition(view_class, view_args, url_args)
    url_args = url_args or []
    return attribute_dict_update(
        viewset,
        'views',
        view_class,
        view_args,
    )
