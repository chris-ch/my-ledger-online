import locale
import logging

_LOG = logging.getLogger('oas.views.google')

from django.shortcuts import redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from google.appengine.api import users


def google_login(request):
    google_user = users.get_current_user()
    next_page = request.GET.get('next', '/')
    _LOG.debug('google user=%s' % users.get_current_user())
    if google_user is None:
        google_login_page = users.create_login_url(next_page)
        _LOG.debug('redirecting to google login page, with next set to "%s"' % next_page)
        return redirect(google_login_page)
    else:
        _LOG.debug('google user authenticated, clearing django auth')
        user = authenticate(username=google_user.email(), password='*')
        login(request, user)
        _LOG.debug('django authenticated: %s' % (('no', 'yes')[request.user.is_authenticated()]))
        _LOG.debug('django user=%s' % request.user)
        _LOG.debug('redirecting to page "%s"' % next_page)
        return redirect(next_page)


def google_logout(request):
    google_logout_page = users.create_logout_url('/')
    logout(request)
    _LOG.debug('logging out google account')
    return redirect(google_logout_page)
