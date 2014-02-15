from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.edit import ModelFormMixin


class ModelFormRedirectMixin(ModelFormMixin):
    """TODO: Documentation"""
    redirects = None
    def form_valid(self, form):
        """
        If the form is valid, redirect to the computed URL

        Overriden to give form.data as argument to get_success_url
        """
        self.object = form.save()

        # Give form data to get_success_url
        return HttpResponseRedirect(self.get_success_url(form.data))

    def redirect_fallback(self):
        return self.object.get_detail_url() or self.object.__class__.get_list_url()

    def get_success_url(self, data = None, debug = True):
        def parse_redirect(destination):
            if isinstance(destination, str):
                # Destination is a string, assume absolute path
                return destination
            elif hasattr(destination, '__call__'):
                # Destination is callable, call with object as arg, and return result
                return destination(self.object)
            else:
                raise ImproperlyConfigured("The redirect target was neither a string nor a callable")

        if self.redirects:
            # We have some redirects defined, let's first try to get the success URL using them
            if data:
                for token, destination in self.redirects.items():
                    if token in data:
                        # Token found in submit data keys
                        return parse_redirect(destination)
            # If at this point, we have not returned
            # it means that no submit data key matched a key in self.redirects

            # We try to use the fallback token
            if None in self.redirects:
                return parse_redirect(self.redirects[None])

        # if at this point we have not returned, it means that :
        #  - no redirects were defined
        #  - OR no form data was submitted
        #  - OR ( no token matched the form data AND no fallback token was defined )

        # We try to find 'next' in form data
        if data and data.get('next'):
            return data.get('next')

        # We try to use success_url
        if self.success_url:
            return parse_redirect(self.success_url)


        # Fallback
        try:
            return self.redirect_fallback()
        except:
            pass

        raise ImproperlyConfigured("No redirect tokens were matched against the form data, no fallback token was found, success_url was not defined, could not get object list url : can't find where to redirect to")
