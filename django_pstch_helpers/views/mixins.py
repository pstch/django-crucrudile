from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render

from django.views.generic import View

from django.views.generic.base import ContextMixin
from django.views.generic.edit import ModelFormMixin

class AuthMixin(View):
    """
    Use this mixin to enforce 'required login' and 'required permissions' attributes.
    
    Arguments:
    required_login -- Boolean, if True, for anonymous users, login form will be rendered instead of page
    required_permissions -- List if permissions, if missing permission, display error message instead of page
    """
    required_login = True
    required_permissions = (None,)

    login_template = "auth/login_required.html"
    perms_template = "auth/permissions_required.html"

    def dispatch(self, request, *args, **kwargs):
        if self.required_login and not request.user.is_authenticated():
            # User not logged in, login required
            return render(request,
                          self.login_template, 
                          {'next' : request.get_full_path(),
                           'login_form_present' : True})

        if self.required_permissions and not request.user.has_perms(self.required_permissions):
            # Missing perm
            return render(request,
                          self.perms_template,
                          {'required_permissions' : self.required_permissions })
            
        # Everything okay, process View
        return super(AuthMixin, self).dispatch(request, *args, **kwargs)

class ModelInfoMixin(ContextMixin):
    """Adds the current model to the template context"""
    def get_context_data(self, **kwargs):
        context = super(ModelInfoMixin, self).get_context_data(**kwargs)
        context['model'] = self.model
        return context

class RedirectMixin(ModelFormMixin):
    """TODO: Documentation"""
    redirects = None
    def form_valid(self, form):
        """
        If the form is valid, redirect to the computed URL
        """
        self.object = form.save()
        raise Exception("test")
        # Give form data to get_success_url
        return HttpResponseRedirect(self.get_success_url(form.data))

    def get_success_url(self, data = None, debug = True):
        def parse_redirect(destination):
            if isinstance(destination, str):
                # Destination is a string, assume absolute path
                return dest
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

            
        # Hard-coded fallback: try to get list view
        try:
            return self.object.__class__.get_list_url()
        except AttributeError:
            pass

        raise ImproperlyConfigured("No redirect tokens were matched against the form data, no fallback token was found, success_url was not defined, could not get object list url : can't find where to redirect to")
