"""
Luna Options HTTP Server side fro handling GET requests
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import LunaOptionsDB as db


class LunaOptionsHTTPServer(BaseHTTPRequestHandler):
    """
    The class for managing the Luna Options HTTP Server Side
    """
    def __init__(self, request, client_address, server):
        self.ticker_template = {
            'ticker': None,
            'comp': None,
            'last_updated': None,
            'sentiment': None,
            'current': None,
            'd_high': None,
            'd_low': None,
            'w_high': None,
            'w_low': None,
            'm_high': None,
            'm_low': None,
            'cur_vol': None,
            'avg_vol': None
        }
        self.db = db.LunaDB()
        super().__init__(request, client_address, server)
        self.port = 42069


    def do_GET(self):
        path = self.path
        query = urlparse(path)
        query = self.query_string(query.query)
        response = self.HTTP_response(query)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes(response, "utf8"))

    def query_string(self, query):
        """
        Manipulates the imported query string and returns a dictionary object with {query:value}
        """
        if query:
            return_dict = {}
            parameters = query.split('&')
            for parameter in parameters:
                parameter = parameter.split('=')
                parameter = tuple(parameter)
                return_dict[parameter[0]] = parameter[1]

            return return_dict

    def HTTP_response(self, query):
        """
        Takes a dictionary object, calls for the data and returns a JSON object for the
        response for the HTTP GET Request
        """
        if query:
            values = query.keys()

            if 'tick' in values:
                response = self.ticker_template.copy()
                ticker = query['tick']
                response['ticker'] = ticker

                data = self.db.get_ticker_info(ticker)
                response.update(data)

                response_json = json.dumps(response)

                return response_json


with HTTPServer(('', 42069), LunaOptionsHTTPServer) as server:
    server.serve_forever()