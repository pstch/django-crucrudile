from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.conf import settings

from django.views.generic import View

from django.views.generic.base import ContextMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import ModelFormMixin

class AuthMixin(View):
    """
    Use this mixin to enforce 'required login' and 'required permissions' attributes.

    'login_template', 'perms_template' and their equivalent in settings.py (AUTH_LOGIN_REQUIRED_TEMPLATE and AUTH_MISSING_PERM_TEMPLATE) may also be callables that will be evaluated at the first request, with the view and the request as arguments.
    settings.py:
    AUTH_LOGIN_REQUIRED_TEMPLATE -- Template used to render the 'login required' page
    AUTH_MISSING_PERM_TEMPLATE -- Template used to render the 'missing permissions' page

    AUTH_EXPAND_PATHS_WITH_APP -- Boolean value, use true to make AuthMixin expand the default paths to include the application name.
    AUTH_LOG_REQ_EXPAND_STRING -- String used to expand the 'login_required' template. Defaults to : '%s/auth/login_required.html'
    AUTH_PERM_REQ_EXPAND_STRING -- String used to expand the 'permissions_required' template. Defaults to : '%s/auth/permissions_required.html'

    Arguments:
    required_login -- Boolean, if True, for anonymous users, login form will be rendered instead of page
    required_permissions -- List if permissions, if missing permission, display error message instead of page

    login_template -- Template used to render the 'login required' page
    perms_template -- Template used to render the 'missing permissions' page
    """
    required_login = True
    required_permissions = (None,)

    with getattr(settings,
                 'AUTH_EXPAND_PATHS_WITH_APP',
                 False) as expand_paths:
        if not expand_paths:
            login_template = getattr(settings,
                                     'AUTH_LOGIN_REQUIRED_TEMPLATE',
                                     'auth/login_required.html')
            perms_template = getattr(settings,
                                     'AUTH_MISSING_PERM_TEMPLATE',
                                     'auth/permissions_required.html')
        else:
            with getattr(settings,
                         'AUTH_LOG_REQ_EXPAND_STRING',
                         '%s/auth/login_required.html') as string:
                login_template = lambda v, r: string % resolve(r.path).app_name
                with getattr(settings,
                         'AUTH_PERM_REQ_EXPAND_STRING',
                         '%s/auth/permissions_required.html') as string:

                perms_template = lambda v, r: string % resolve(r.path).app_name

    def dispatch(self, request, *args, **kwargs):
        with login_template as c:
            if callable(c):
                c = c(self, request)
                if callable(c):
                    raise ImproperlyConfigured(
                        "Calling AUTH_LOGIN_REQUIRED_TEMPLATE returned a callable.")
        with perms_template as c:
            if callable(c):
                c = c(self, request)
                if callable(c):
                    raise ImproperlyConfigured(
                        "Calling AUTH_MISSING_PERM_TEMPLATE returned a callable.")

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

class SelectRelatedMixin(MultipleObjectMixin):
    select_related = None
    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                manager = queryset
        elif self.model is not None:
            manager = self.model._default_manager
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )

        if self.select_related is not None:
            queryset = manager.select_related(*self.select_related).all()
        else:
            queryset = manager.all()

        return queryset


class ExtraContextMixin(ContextMixin):
    extra_context = {}
    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        if callable(self.extra_context):
            context.update(self.extra_context(self, context))
        else:
            context.update(self.extra_context)
        return context


class ModelInfoMixin(ExtraContextMixin, ContextMixin):
    """Adds the current model to the template context"""
    def get_context_data(self, **kwargs):
        context = super(ModelInfoMixin, self).get_context_data(**kwargs)
        if hasattr(self, 'model'):
            context['model'] = self.model
        if hasattr(self, 'models'):
            context['models'] = self.models
        return context

class RedirectMixin(ModelFormMixin):
    """TODO: Documentation"""
    redirects = None
    def form_valid(self, form):
        """
        If the form is valid, redirect to the computed URL
        """
        self.object = form.save()

        # Give form data to get_success_url
        return HttpResponseRedirect(self.get_success_url(form.data))

    def redirect_fallback(self):
        try:
            url = self.object.get_detail_url()
            assert url
        except:
            url = self.object.__class__.get_list_url()
            assert url
        return url


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


        # Fallback
        try:
            return self.redirect_fallback()
        except:
            pass

        raise ImproperlyConfigured("No redirect tokens were matched against the form data, no fallback token was found, success_url was not defined, could not get object list url : can't find where to redirect to")
