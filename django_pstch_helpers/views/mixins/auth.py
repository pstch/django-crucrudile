from django.core.exceptions import ImproperlyConfigured
from django.views.generic import View
from django.shortcuts import render

from .prefix import TemplateAppPrefixMixin

class AuthMixin(View):
    """
    Use this mixin to enforce 'required login' and 'required permissions' attributes.

    settings.py:
    AUTH_LOGIN_REQUIRED_TEMPLATE -- Template used to render the 'login required' page
    AUTH_MISSING_PERM_TEMPLATE -- Template used to render the 'missing permissions' page

    Arguments:
    required_login -- Boolean, if True, for anonymous users, login form will be rendered instead of page
    required_permissions -- List if permissions, if missing permission, display error message instead of page

    login_template -- Template used to render the 'login required' page
    perms_template -- Template used to render the 'missing permissions' page

    login_template_no_prefix -- Same as above, but will be prefixed using TemplateAppPrefixMixin. Is only used if login_template is None.
    perms_template_no_prefix -- Same as above, but will be prefixed using TemplateAppPrefixMixin. Is only used if perms_template is None.
    """
    required_login = True
    required_permissions = (None,)

    login_template = None
    perms_template = None

    login_template_no_prefix = 'auth/login_required.html'
    perms_template_no_prefix = 'auth/permissions_required.html'

    def expand_template_name(self, no_prefix_name):
        prefix_mixin = TemplateAppPrefixMixin()
        # we use this to have TemplateAppPrefixMixin use get_template_names() for us, which will be given the unprefixed template path as argument, and will return the prefixed template path.
        # get_template_names() will get the prefix from the settings, in PER_APP_TEMPLATE_PREFIX["<application name>"]. If this is not set, or if the application name is not present in the keys, the application name will be used as prefix.
        # the application name is urlresolvers.resolve(path).app_name
        prefix_mixin.request = self.request
        prefix_mixin.template_name =
        prefix_mixin.template_name_no_prefix = no_prefix_name
        return prefix_mixin.get_template_names()[0]

    def dispatch(self, request, *args, **kwargs):
        login_template = self.login_template or self.expand_template_name(self.login_template_no_prefix)
        perms_template = self.perms_template or self.expand_template_name(self.perms_template_no_prefix)

        if self.required_login and not request.user.is_authenticated():
            # User not logged in, login required
            return render(request,
                          login_template,
                          {'next' : request.get_full_path(),
                           'login_form_present' : True})

        if self.required_permissions and not request.user.has_perms(self.required_permissions):
            # Missing perm
            return render(request,
                          perms_template,
                          {'required_permissions' : self.required_permissions })

        # Everything okay, process View
        return super(AuthMixin, self).dispatch(request, *args, **kwargs)
