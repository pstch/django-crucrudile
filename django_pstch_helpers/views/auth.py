"""
#TODO: Add module docstring
"""
#pylint: disable=R0901, R0904
import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext as _

from .mixins.template import TemplateResponseMixin

class LoginView(TemplateResponseMixin, View):
    """
    #TODO: Add class docstring
    """
    fallback_redirect_to = "home"
    template_name = "auth/login_required.html"

    def redirect(self, request):
        """
        #TODO: Add method docstring
        """
        if hasattr(request.POST, 'next'):
            return HttpResponseRedirect(request.POST['next'])
        else:
            return HttpResponseRedirect(reverse(self.fallback_redirect_to))

    def get(self, request):
        """
        #TODO: Add method docstring
        """
        return render(request,
                      self.get_template_names(),
                      {'login_form_present' : True})

    def post(self, request):
        """
        #TODO: Add method docstring
        """
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                # success
                messages.success(
                    request,
                    _("Login successful ! User %s connected at %s") \
                    % (user.username, datetime.datetime.now())
                )
                return self.redirect(request)
            else:
                # disabled account
                messages.error(
                    request,
                    _("This account (%s) is disabled.") \
                    % user.username
                )
                return self.redirect(request)
        else:
            # invalid login
            messages.error(request, _("Invalid credentials. Please try again."))
            return self.redirect(request)


class LogoutView(View):
    """
    #TODO: Add class docstring
    """
    redirect_to = None
    fallback_redirect_to = "home"
    def get(self, request):
        """
        #TODO: Add method docstring
        """
        logout(request)
        messages.success(request, "You have been logged out.")

        if self.redirect_to:
            return HttpResponseRedirect(reverse(self.redirect_to))
        else:
            return HttpResponseRedirect(
                getattr(request.META,
                        'HTTP_REFERER',
                        reverse(self.fallback_redirect_to)))
