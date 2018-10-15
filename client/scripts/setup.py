import logging
import http.client

host = 'django'
port = 8000


def run():
    logging.info('connecting to %s:%s', host, port)

    conn = http.client.HTTPConnection(host=host, port=port)

    payload = """
{
    "code": "le001",
    "name": "le001",
    "is_individual": 0,
    "currency": "EUR",
    "user": "test001",
    "description": "legal entity 001"
}
"""

    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        'Authorization': "Basic b2FzOm9hcw==",
        'Cache-Control': "no-cache",
        'Postman-Token': "8fb9cf48-e7aa-4135-bd9f-306349e4a180"
    }

    conn.request("POST", "/legal_entities.json", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode('utf-8'))


if __name__ == '__main__':
    run()
