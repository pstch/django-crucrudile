class RouteArguments(list):
    """Route URL arguments specification. Generates argument regexes from
    a given argument specification. This allows you to give the possible
    URL arguments to be used in the URL, and :func:`get_regexs` will
    return a regex for each argument combination found.

    """
    separator = "/"

    opt_separator = "/?"
    required_default = True

    @classmethod
    def test_input(cls, input_data):
        return isinstance(input_data, list)

    def __init__(self, arguments):
        """Initialize route arguments, takes the argument specification (list)
        as argument

        """
        super().__init__(arguments or [])
        self.required = None
        self.init_regexs()

    def get_separator(self, required=None):
        """Get the argument separator to use according to the :attr:`required`
        argument

        :argument required: If False, will return the optional
                            argument separator instead of the regular
                            one. Default is the value of
                            :attr:`required_default`.
        :type required: bool
        """
        if required is None:
            if self.required is None:
                required = self.required_default
            else:
                required = self.required
        if required:
            return self.separator
        else:
            return self.opt_separator

    def clean(self):
        """Yield "cleaned" items. Cleaning an item implies converting it to a
        2-tuple (with :attr:`required_default` and the item) if it's
        not one, then wrapping the original item (now the 2nd element
        of the tuple) in a single item list if it's a string.

        """
        # RouteArguments is itself a list, so we can just iterate over
        # self to get the original items
        for item in self:
            if not isinstance(item, tuple):
                # not a tuple, use required_default to build one
                required, arg_spec = self.required_default, item
            else:
                required, arg_spec = item

            if isinstance(arg_spec, str):
                arg_spec = [arg_spec, ]

            yield required, arg_spec

    def init_regexs(self):
        """Sets an instance attribute (``required``) contaning a boolean
        indicating if the arguments in this object are "required"
        (i.e. they will always be present in the regex), and another
        attribute (``arg_combs``) containing a list of argument URL
        regexes.

        The returned boolean value is useful to know if this regex
        part should be joined to another regex part using an optional
        separator, instead of the regular, required, separator.

        In its implementation, this runs a variant of the cartesian
        product on the list items to get all the possible argument
        combinations.

        """

        # arg_combs need an empty string so that the recursive list
        # comprehension below works

        # it needs to start with an empty string so that it can be
        # joined to append arguments

        # it also matches with this function behaviour : if no
        # arguments are defined (so the below loop doesn't run), we
        # still need an URL regex (with no arguments), which will be
        # made from the empty string singleton returned by this
        # function.
        arg_combs = ['']

        # False at the beginning, will be set *while* iterating over
        # the arguments
        is_required = False

        # iterate over the cleaned items
        for required, possible_args_list in self.clean():
            # a single required argument specifications is enough to
            # mark the whole object as required
            if required:
                is_required = True
            # get the argument separator
            separator = self.get_separator(required)

            arg_combs = [
                separator.join(filter(None, [comb, arg]))
                for comb in arg_combs
                for arg in possible_args_list
            ]

        self.arg_combs = arg_combs
        self.required = is_required
