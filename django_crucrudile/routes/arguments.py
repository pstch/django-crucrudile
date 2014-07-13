from abc import ABCMeta, abstractmethod


class BaseArgParser(list, metaclass=ABCMeta):
    separator = "/"
    opt_separator = "/?"
    required_default = True

    @abstractmethod
    def __init__(self, arg_regexs,
                 required_default=None,
                 separator=None,
                 opt_separator=None,
                 **kwargs):
        """Initialize route arguments, takes the argument specification (list)
        as argument

        """
        self.required = False
        if required_default:
            self.required_default = required_default
        if separator:
            self.separator = separator
        if opt_separator:
            self.opt_separator = opt_separator

        super().__init__(arg_regexs)

    def get_separator(self, required=None):
        """Get the argument separator to use according to the :attr:`required`
        argument

        :argument required: If False, will return the optional
                            argument separator instead of the regular
                            one. Default is True.
        :type required: bool
        """
        if required is None:
            required = self.required_default
        if required:
            return self.separator
        else:
            return self.opt_separator


class SimpleArgParser(BaseArgParser):
    """Route URL arguments specification. Generates argument regexes from
    a given argument specification. This allows you to give the possible
    URL arguments to be used in the URL, and :func:`get_regexs` will
    return a regex for each argument combination found.

    """
    def __init__(self, specs, **kwargs):
        def _get_parts_lists(regexs, args):
            for regex in regexs:
                for arg in args:
                    yield regex, arg

        def _filter_none(parts_lists):
            for parts_list in parts_lists:
                yield filter(None, parts_list)

        def _join_with_sep(parts_lists, required):
            sep = self.get_separator(required)
            for parts_list in parts_lists:
                yield sep.join(parts_list)

        def _cartesian_product(required, regexs, args):
            parts_lists = _get_parts_lists(regexs, args)
            parts_lists = _filter_none(parts_lists)
            return _join_with_sep(parts_lists)


        # arg_combs need an empty string so that the recursive list
        # comprehension below works

        # it needs to start with an empty string so that it can be
        # joined to append arguments

        # it also matches with this function behaviour : if no
        # arguments are defined (so the below loop doesn't run), we
        # still need an URL regex (with no arguments), which will be
        # made from the empty string singleton returned by this
        # function.
        regexs = ['']

        # False at the beginning, will be set *while* iterating over
        # the arguments
        # iterate over the cleaned items
        specs = self.clean(specs)
        specs = self.mark_required(specs)

        for required, args in specs:
            regexs = _cartesian_product(required, regexs, args)

        super().__init__(regexs, **kwargs)

    def clean(self, arg_specs):
        """Yield "cleaned" arg specification. Cleaning an arg specification
        implies converting it to a 2-tuple (with
        :attr:`required_default` and the original item) if it's not
        one, then wrapping the original item (now the 2nd element of
        the tuple) in a single item list if it's a string.

        """
        # RouteArguments is itself a list, so we can just iterate over
        # self to get the original items
        for item in arg_specs:
            if not isinstance(item, tuple):
                # not a tuple, use required_default to build one
                required, arg_spec = self.required_default, item
            else:
                required, arg_spec = item

            if isinstance(arg_spec, str):
                arg_spec = [arg_spec, ]

            yield required, arg_spec

    def mark_required(self, arg_specs):
        for required, arg_spec in arg_specs:
            if required:
                self.required = True
            yield required, arg_spec
