import os
import time
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from function import handler
from graphql import client

#  removed os.environ to test with hardcoded values
#  - nadro-j
hostName = "0.0.0.0"
PORT = 8000
GRAPHQL_URL = "https://admin.basehash.com/graphql"
GraphQL = client.GraphQLClient(GRAPHQL_URL)

class FaasContext:
    def __init__(self, client):
        self.client = client

class FaasServer(BaseHTTPRequestHandler):
    def getHeader (self, header):
        head = self.headers.get(header)
        return head[0] if head else None

    def setJobHeaders(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("X-Worker-Id", self.getHeader('X-Worker-Id'))
        self.send_header("X-Job-Id", self.getHeader('X-Job-Id'))
        self.end_headers()

    def sendError(self, msg):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("X-Worker-Id", self.getHeader('X-Worker-Id'))
        self.send_header("X-Job-Id", self.getHeader('X-Job-Id'))
        self.send_header("X-Job-Error", True)
        self.end_headers()
        self.wfile.write(json.dumps({'message': msg}))

    def getReqParams(self):
        length = int(self.headers.get('content-length'))

        if length > 0:
            content = self.rfile.read(length)
            return content
        else:
            return json.loads('{}')

    def do_POST(self):
        params = self.getReqParams()
        try:
            ctx = FaasContext(GraphQL)
            val = handler.handle(params, ctx)
            self.setJobHeaders()
            self.wfile.write(bytes(str(val), encoding='utf8'))
        except Exception as e:
            self.sendError(str(e))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, PORT), FaasServer)
    print("Server started http://%s:%s" % (hostName, PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
