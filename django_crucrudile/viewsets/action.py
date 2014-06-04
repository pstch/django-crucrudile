def provides(viewset, view_class, view_args):
    viewset.views[view_class].update(view_args)
