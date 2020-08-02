from http.client import HTTPConnection

def testrq(obj):
    c = HTTPConnection('78.141.196.199', 8000)
    c.connect()
    c.request("POST", "/", body=obj, headers={})
    response_bytes = c.getresponse().read()
    response_string = response_bytes.decode('utf-8')
    return response_string

if __name__ == '__main__':
    print (testrq("getUsers"))