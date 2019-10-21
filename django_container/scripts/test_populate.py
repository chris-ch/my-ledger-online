from oas import models


def run(*args):
    import http.client

    conn = http.client.HTTPConnection("127,0,0,1")

    payload = "{\n\t\"code\": \"le001\",\n\t\"name\": \"le001\",\n\t\"is_individual\": 0,\n\t\"currency\": \"EUR\"," \
              "\n\t\"owner\": \"test001\"\n}"

    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        'Authorization': "Basic b2FzOm9hcw==",
        'Cache-Control': "no-cache",
        'Postman-Token': "407f3a6d-c286-4400-ba26-7a91e0353934"
    }

    conn.request("POST", "legal_entities.json", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
