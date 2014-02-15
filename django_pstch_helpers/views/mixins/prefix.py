from django.core.urlresolvers import resolve
from django.conf import settings

class TemplateAppPrefixMixin():
    template_name = None
    template_name_no_prefix = None
    join_by = '/'

    def get_template_names(self):
        if not self.template_name_no_prefix or self.template_name:
            return self.template_name

        app_name = resolve(self.request.path).app_name

        app_path_part = getattr(getattr(settings,
                                        "PER_APP_TEMPLATE_PREFIX",
                                        {}),
                                app_name,
                                app_name)

        return [[app_path_part, self.template_name_no_prefix].join(self.join_by)]
