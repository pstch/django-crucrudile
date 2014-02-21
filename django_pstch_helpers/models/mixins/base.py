from django.core.urlresolvers import reverse

class ModelInfoMixin(object):
    #TODO: Write tests for this class, with a sample Model where we test each function
    @classmethod
    def _get_objects(self):
        try:
            objects = self.objects
            return objects
        except AttributeError:
            raise ImproperlyConfigured("Could not find manager : \"objects\" not present on the current object. Check that ModelInfoMixin is used on a Model.")

    @classmethod
    def _get_meta(self):
        try:
            _meta = self._meta
            return _meta
        except AttributeError:
            raise ImproperlyConfigured("Could not find Meta class : \"_meta\" not present on the current object. Check that ModelInfoMixin is used on a Model.")

    @classmethod
    def get_verbose_name(self):
        _meta = self._get_meta()
        return _meta.verbose_name
    @classmethod
    def get_count(self):
        objects = self._get_objects()
        return self.objects.count()
    @classmethod
    def get_model_name(self):
        _meta = self._get_meta()
        return _meta.model_name

class AutoPatternsMixin(ModelInfoMixin):
    #TODO: Write tests for this class, with a sample Model where we test each function
    def get_url_name(self):
        return self.get_model_name()
    def get_url_prefix(self):
        return None
    def get_views(self):
        """
        Base get_views() function, must be here for the MRO. Returns a
        dictionary containing the views defined by each ModelMixin.

        Each ModelMixin should override this function and
        use contribute_viewset_to_views to add the data
        from its ViewSet.

        Usually called with super(..., self).get_views()
        """
        return {} # hey, BASE_VIEWS
    def get_view_args(self):
        """
        Similar to get_views(), but here we don't use a function like
        contribute_viewset_to_views. Returns a dictionary containing
        the view arguments defined by each ModelMixin and by the Model
        classes. Each value should also be a dictionary
        """
        return {}
    def get_url_namespaces(self):
        return []
    def _make_url_name(self, action):
        return make_url_name(self.get_url_namespaces(),
                             self.get_url_name(),
                             action)
    def get_url(self, action, args=None):
        return reverse(self._make_url_name(action),
                           args=args)

