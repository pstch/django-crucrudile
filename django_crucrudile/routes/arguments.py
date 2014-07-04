class RouteArguments(list):
    separator = "/"
    opt_separator = "/?"
    required = True

    def __init__(self, arguments):
        super().__init__(arguments)

    def get_separator(self, required):
        if required:
            return self.separator
        else:
            return self.opt_separator

    def clean(self):
        for item in self:
            if isinstance(item, (str, list)):
                required, arg_spec = self.required, item
            else:
                required, arg_spec = item

            if isinstance(arg_spec, str):
                arg_spec = [arg_spec, ]

            yield required, arg_spec

    def get_regexs(self):
        arg_combs = [(False, '')]

        for required, arg_spec in self.clean():
            separator = self.get_separator(required)

            arg_combs = [
                (
                    required or comb_required,
                    separator.join(
                        filter(None, [arg_comb, arg])
                    )
                )

                for comb_required, arg_comb in arg_combs
                for arg in arg_spec
            ]
        return arg_combs
