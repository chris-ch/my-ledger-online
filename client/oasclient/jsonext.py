import logging
import json

import mechanize
import uuid

_LOG = logging.getLogger('jsonext')


def _types_gen(T):
    yield T
    if hasattr(T, 't'):
        for l in T.t:
            yield l
            if hasattr(l, 't'):
                for ll in _types_gen(l):
                    yield ll


class LoginFailedException(Exception):
    pass


class Type(type):
    """ A rudimentary extension to `type` that provides polymorphic
    types for run-time type checking of JSON data types. IE:
    
    assert type(u'') == String
    assert type('') == String
    assert type('') == Any
    assert Any.kind('') == String
    assert Any.decode('str') == String
    assert Any.kind({}) == Object
    """

    def __init__(self, *args, **kwargs):
        type.__init__(self, *args, **kwargs)

    def __eq__(self, other):
        for T in _types_gen(self):
            if isinstance(other, Type):
                if T in other.t:
                    return True
            if type.__eq__(T, other):
                return True
        return False

    def __str__(self):
        return getattr(self, '_name', 'unknown')

    def N(self, n):
        self._name = n
        return self

    def I(self, *args):
        self.t = list(args)
        return self

    def kind(self, t):
        if type(t) is Type:
            return t
        ty = lambda t: type(t)
        if type(t) is type:
            ty = lambda t: t
        return reduce(
            lambda L, R: R if (hasattr(R, 't') and ty(t) == R) else L,
            filter(lambda T: T is not Any,
                   _types_gen(self)))

    def decode(self, n):
        return reduce(
            lambda L, R: R if (str(R) == n) else L,
            _types_gen(self))


# JSON primitives and data types
Object = Type('Object', (object,), {}).I(dict).N('obj')
Number = Type('Number', (object,), {}).I(int, long).N('num')
Boolean = Type('Boolean', (object,), {}).I(bool).N('bit')
String = Type('String', (object,), {}).I(str, unicode).N('str')
Array = Type('Array', (object,), {}).I(list, set, tuple).N('arr')
Nil = Type('Nil', (object,), {}).I(type(None)).N('nil')
Any = Type('Any', (object,), {}).I(Object, Number, Boolean, String, Array, Nil).N('any')


class ServiceProxy(object):
    def __init__(self, server,
                 service_path,
                 port=80,
                 protocol='http',
                 service_name=None,
                 version='2.0',
                 browser=None):
        self.__version = str(version)
        self.__protocol = protocol
        self.__service_path = service_path
        if not service_path.endswith('/'):
            self.__service_path += '/'

        self.__server = server
        self.__port = str(port)
        self.__service_name = service_name
        if browser is None:
            self.__browser = mechanize.Browser()
            self.__browser.set_handle_robots(False)
            self.__browser.logged_in = False
        else:
            self.__browser = browser

        def default_login(browser, uri):
            browser.logged_in = True
            return True

        self.__login_procedure = default_login

    def __getattr__(self, name):
        if self.__service_name != None:
            name = "%s.%s" % (self.__service_name, name)

        sp = JSONMethodSet(self.__server,
                           self.__service_path,
                           self.__login_procedure,
                           self.__browser,
                           self.__port,
                           self.__protocol,
                           name,
                           self.__version
                           )
        return sp

    def set_login_procedure(self, login_procedure):
        self.__login_procedure = login_procedure


class JSONRemoteException(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg


class JSONMethodSet(object):
    def __init__(self, server,
                 service_path,
                 login_proc,
                 browser,
                 port,
                 protocol,
                 service_name,
                 version
                 ):
        self.__version = str(version)
        self.__protocol = protocol
        self.__service_path = service_path
        self.__server = server
        self.__port = port
        self.__service_name = service_name
        self.__browser = browser
        self.__login_procedure = login_proc

    def __repr__(self):
        return repr({'jsonrpc': self.__version,
                     'method': self.__service_name})

    def __call__(self, *args, **kwargs):

        server_uri = '%s://%s:%s' % (self.__protocol, self.__server, self.__port)
        print
        server_uri
        if not self.__browser.logged_in:
            _LOG.info('authenticating on %s' % server_uri)
            login_status = self.__login_procedure(self.__browser, server_uri)
            if not login_status:
                _LOG.error('login failed')
                raise LoginFailedException
            else:
                _LOG.debug('login succeeded')
                self.__browser.logged_in = True

        params = kwargs if len(kwargs) else args
        if Any.kind(params) == Object and self.__version != '2.0':
            raise Exception('Unsupport arg type for JSON-RPC 1.0 ')

        uuid1 = str(uuid.uuid1())
        params = {'jsonrpc': self.__version,
                  'method': self.__service_name,
                  'params': params,
                  'id': uuid1
                  }
        dumps = json.dumps(params)

        service_url = server_uri + '/' + self.__service_path

        _LOG.debug('calling url: %s' % service_url)
        # _LOG.debug('using params: <JSON>%s</JSON>' % dumps)

        response = self.__browser.open(service_url, data=dumps)
        content = response.read()

        # _LOG.debug('raw response: <RAW>%s</RAW>' % content)

        json_response = json.loads(content)

        if json_response.has_key('error'):
            code = json_response['error']['code']
            message = json_response['error']['message']
            srv_msg = 'Remote Error %s: %s' % (code, message)
            _LOG.error('error response: %s' % srv_msg)
            raise JSONRemoteException(srv_msg)

        return json_response['result']
