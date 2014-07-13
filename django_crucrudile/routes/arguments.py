from abc import ABCMeta, abstractmethod

class BaseArgParser(list, metaclass=ABCMeta):
    separator = "/"
    opt_separator = "/?"
    required_default = True

    def __init__(self,
                 arg_specs, required_default=None,
                 separator=None, opt_separator=None,):
        """Initialize route arguments, takes the argument specification (list)
        as argument

        """
        self.arg_specs = arg_specs
        self.required = False
        if required_default:
            self.required_default = required_default
        if separator:
            self.separator = separator
        if opt_separator:
            self.opt_separator = opt_separator

        super().__init__(self.get_arg_regexs())

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

    @abstractmethod
    def make_arg_regexs(self):
        pass

class SimpleArgParser(BaseArgParser):
    """Route URL arguments specification. Generates argument regexes from
    a given argument specification. This allows you to give the possible
    URL arguments to be used in the URL, and :func:`get_regexs` will
    return a regex for each argument combination found.

    """
    def clean_arg_specs(self):
        """Yield "cleaned" arg specification. Cleaning an arg specification
        implies converting it to a 2-tuple (with
        :attr:`required_default` and the original item) if it's not
        one, then wrapping the original item (now the 2nd element of
        the tuple) in a single item list if it's a string.

        """
        # RouteArguments is itself a list, so we can just iterate over
        # self to get the original items
        for item in self.arg_specs:
            if not isinstance(item, tuple):
                # not a tuple, use required_default to build one
                required, arg_spec = self.required_default, item
            else:
                required, arg_spec = item

            if isinstance(arg_spec, str):
                arg_spec = [arg_spec, ]

            yield required, arg_spec

    def make_arg_regexs(self):
        """Returns a list of argument URL regexes.

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
        # iterate over the cleaned items
        for required, possible_args_list in self.clean():
            # a single required argument specifications is enough to
            # mark the whole object as required
            if required:
                self.required = True
            # get the argument separator
            separator = self.get_separator(required)

            arg_combs = [
                separator.join(filter(None, [comb, arg]))
                for comb in arg_combs
                for arg in possible_args_list
            ]
        return arg_combs
