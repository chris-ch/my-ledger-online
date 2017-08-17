import logging

_LOG = logging.getLogger('oasclient')


class LoginError:
    def __init__(self, message=''):
        self.message = message

    def __repr__(self):
        return self.message


def login_sequence(user, password=None, user_input_name='user',
                   password_input_name='password', auto_register=True,
                   login_path='/login', success_url='http://mysite.com'):
    """
    Creating a callback function used by jsonext
    for authenticating a user on the RPC server.
    """

    def login_phase(browser, server_uri):
        # asking for a login page
        login_page = browser.open(server_uri + login_path)

        # posting login details
        browser.select_form(nr=0)
        browser.set_value(user, user_input_name)

        if password is not None:
            try:
                browser.set_value(password, password_input_name)

            except:
                msg = 'unable to set password (field "%s")' % password_input_name
                _LOG.error(msg)
                raise LoginError(msg)

        auth_result = browser.submit()
        if auth_result.geturl().startswith(success_url):
            return True

        else:
            return False

    return login_phase
