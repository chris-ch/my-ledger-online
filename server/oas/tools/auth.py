import logging

_LOG = logging.getLogger('oas.tools.auth')

from google.appengine.api import users

from django.contrib.auth import models
from django.conf import settings


class GoogleAuthBackend(object):
    """
    Authenticates against Google accounts.
    """

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        google_user = users.get_current_user()
        _LOG.debug('updating django user with google user: %s' % google_user)
        user = None
        if google_user:
            # returns the app user if succesfully authentified with Google
            try:
                user = models.User.objects.get(username=username)

            except models.User.DoesNotExist:
                # Creates a new user. Note that we can set password
                # to anything, because it won't be checked
                user = models.User(username=username, password='*')
                user.save()

        return user

    def get_user(self, user_id):
        try:
            return models.User.objects.get(pk=user_id)

        except models.User.DoesNotExist:
            return None
