import http.client

conn = http.client.HTTPConnection("127,0,0,1")

payload = "{\n\t\"code\": \"le001\",\n\t\"name\": \"le001\",\n\t\"is_individual\": 0,\n\t\"currency\": \"EUR\",\n\t\"owner\": \"test001\"\n}"

headers = {
    'Accept': "application/json",
    'Content-Type': "application/json",
    'Authorization': "Basic b2FzOm9hcw==",
    'Cache-Control': "no-cache",
    'Postman-Token': "8fb9cf48-e7aa-4135-bd9f-306349e4a180"
    }

conn.request("POST", "legal_entities.json", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
