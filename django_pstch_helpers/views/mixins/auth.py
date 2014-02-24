"""
#TODO: Add module docstring
"""
from django.shortcuts import render

from .template import TemplateResponseMixin

class AuthMixin(object):
    """
    Use this mixin to enforce 'required login' and 'required permissions'
    attributes.

    settings.py:
    AUTH_LOGIN_REQUIRED_TEMPLATE
      -- Template used to render the 'login required' page
    AUTH_MISSING_PERM_TEMPLATE
      -- Template used to render the 'missing permissions' page

    Arguments:
    required_login -- Boolean
      If True, for anonymous users, login form will be rendered instead of page
    required_permissions -- List
      If user lacks a permission in this list :
        display error message instead of page

    login_template -- Template used to render the 'login required' page
    perms_template -- Template used to render the 'missing permissions' page

    login_template_no_prefix -- if True :
      login_template will be prefixed using TemplateAppPrefixMixin.
      Is only used if login_template is None.
    perms_template_no_prefix -- if True :
      perms_template will be prefixed using TemplateAppPrefixMixin.
      Is only used if perms_template is None.
    """
    #pylint: disable=R0903
    required_login = True
    required_permissions = (None,)

    perms_template = None

    login_template_add_prefix = True
    perms_template_add_prefix = True

    def dispatch(self, request, *args, **kwargs):
        """
        #TODO: Add method docstring
        """
        def expand_template_name(name):
            """
            We use this to have TemplateResponseMixin use
            get_template_names() for us, which will be given the
            unprefixed template path as argument, and will return
            the prefixed template path.

            get_template_names() will get the prefix from the
            settings, in :
              PER_APP_TEMPLATE_PREFIX["<application name>"]

            If this is not set, or if the application name
            is not present in the keys, the application name will be
            used as prefix.

            The application name is obtained using :
              urlresolvers.resolve(path).app_name
            """

            template_mixin = TemplateResponseMixin()
            template_mixin.request = request
            template_mixin.template_name = name
            template_mixin.template_name_add_prefix = True

            return template_mixin.get_template_names()[0]

        login_template = self.login_template if not \
                         self.login_template_add_prefix else \
                         expand_template_name(self.login_template)
        perms_template = self.perms_template if not \
                         self.perms_template_add_prefix else \
                         expand_template_name(self.perms_template)

        if self.required_login and \
           not request.user.is_authenticated():
            # User not logged in, login required
            return render(request,
                          login_template,
                          {'next' : request.get_full_path(),
                           'login_form_present' : True})

        if self.required_permissions and \
           not request.user.has_perms(self.required_permissions):
            # Missing perm
            return render(request,
                          perms_template,
                          {'required_permissions' : self.required_permissions})

        # Everything okay, process View
        return super(AuthMixin, self).dispatch(request, *args, **kwargs)
