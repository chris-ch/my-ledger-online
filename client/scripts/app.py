import falcon
from wsgiref import simple_server


class HelloResource(object):

    @staticmethod
    def on_get(req, resp):
        resp.status = falcon.HTTP_200
        resp.body = 'Hello World!'


if __name__ == '__main__':
    api = falcon.API()
    api.add_route('/', HelloResource())
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
