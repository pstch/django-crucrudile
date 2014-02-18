from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from django.views.generic.base import TemplateResponseMixin

class TemplateAppPrefixMixin():
    """
    This works in the same way as TemplateMixin, but is not specific to a single object. get_template_names() will prefix the template name in template_name_no_prefix if and only if template_name is not None.

    get_template_names() will get the prefix from the settings, in PER_APP_TEMPLATE_PREFIX["<application name>"]. If this is not set, or if the application name is not present in the keys, the application name will be used as prefix.

    Note that get_template_names() requires the 'request' attribute set on 'self' (to get app_name from the request path)
    """
    request = None
    template_name = None
    template_name_no_prefix = None
    template_join_by = '/'

    def __init__(self, request):
        # TODO: Find the conventional way of doing this
        for arg in kwargs:
            if hasattr(self, arg):
                setattr(self, arg, kwargs.pop(arg))
            else:
                raise Exception("%s is not a valid attribute to %s" % (arg, self.__class__.split('.')[:1]))

    def get_template_names(self):
        if not self.template_name_no_prefix or self.template_name:
            return self.template_name

        app_name = resolve(self.request.path).app_name

        app_path_part = getattr(getattr(settings,
                                        "PER_APP_TEMPLATE_PREFIX",
                                        {}),
                                app_name,
                                app_name)

        return [[app_path_part, self.template_name_no_prefix].join(self.template_join_by)]

class TemplateMixin():
    template_name = None
    template_name_add_prefix = False
    template_join_by = '/'
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

            # Let's also init TemplateAppPrefix if we need it, and an utility function
            if self.template_name_add_prefix:
                prefix_mixin = TemplateAppPrefixMixin(
                    request = self.request,
                    template_join_by = self.template_join_by
                )
            def prefix(name):
                prefix_mixin.template_name_no_prefix = name
                name = prefix_mixin.get_template_names()[0]

            # If self.template_name_field is set, grab the value of the field
            # of that name from the object; this is the most specific template
            # name, if given.
            if self.object and self.template_name_field:
                name = getattr(self.object, self.template_name_field, None)
                if name:
                    if self.template_name_add_prefix:
                        name = prefix(name)
                    names.insert(0, name)

            # The least-specific option is the default <app>/<model>_detail.html;
            # only use this if the object in question is a model.

            # The first thing to do is to try to get the model name
            model_name = None
            if isinstance(self.object, models.Model):
                # we have an object defined, let's use this
                model_name = self.object.get_model_name()
            elif hasattr(self, 'model') and self.model is not None and issubclass(self.model, models.Model):
                # no object, but model is a Model class !
                model_name = self.model.get_model_name()
            if model_name:
                name = "%s%s.html" % (model_name, self.template_name_suffix)
                if self.template_name_add_prefix:
                    name = prefix(name)
                names.append(name)


            # If we still haven't managed to find any template names, we should
            # re-raise the ImproperlyConfigured to alert the user.
            if not names:
                raise
        return names

