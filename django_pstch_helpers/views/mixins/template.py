from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from django.views.generic.base import TemplateResponseMixin

class TemplateMixin(SingleObjectTemplateResponseMixin):
    def get_template_names(self):
        """
        Return a list of template names to be used for the request. May not be
        called if render_to_response is overridden. Returns the following list:
        * the value of ``template_name`` on the view (if provided)
        * the contents of the ``template_name_field`` field on the
          object instance that the view is operating upon (if available)
        * ``<app_label>/<object_name><template_name_suffix>.html``
        """
        try:
            names = super(SingleObjectTemplateResponseMixin, self).get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []
            # If self.template_name_field is set, grab the value of the field
            # of that name from the object; this is the most specific template
            # name, if given.
            if self.object and self.template_name_field:
                name = getattr(self.object, self.template_name_field, None)
                if name:
                    names.insert(0, name)

            app_path_part = getattr(getattr(settings,
                                            "PER_APP_TEMPLATE_PREFIX",
                                            {}),
                                    self.object._meta.app_name,
                                    self.object._meta.app_name)

            # The least-specific option is the default <app>/<model>_detail.html;
            # only use this if the object in question is a model.
            if isinstance(self.object, models.Model):
                names.append("%s/%s%s.html" % (
                    app_path_part,
                    self.object._meta.model_name,
                    self.template_name_suffix
                ))
            elif hasattr(self, 'model') and self.model is not None and issubclass(self.model, models.Model):
                names.append("%s/%s%s.html" % (
                    app_path_part,
                    self.model._meta.model_name,
                    self.template_name_suffix
                ))
            # If we still haven't managed to find any template names, we should
            # re-raise the ImproperlyConfigured to alert the user.
            if not names:
                raise
        return names

class TemplateMixin(SingleObj)
