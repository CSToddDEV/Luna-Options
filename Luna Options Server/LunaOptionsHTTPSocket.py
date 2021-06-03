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
            'avg_vol': None,
            'current_IV': None
        }
        self.db = db.LunaDB()
        super().__init__(request, client_address, server)
        self.port = 42069

    def close_server(self, server_obj):
        """
        Closes HTTP Server
        """
        server_obj.shutdown()
        server_obj.socket.close()

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

    def tick_response(self, response, query):
        """
        Updates HTTP_Response with ticker data, returns response object
        """
        response.update(self.ticker_template.copy())
        ticker = query['tick']
        ticker = ticker.lower()
        response['ticker'] = ticker

        data = self.db.get_ticker_info(ticker)
        response.update(data)

        return response

    def options_response(self, response, query):
        """
        Updates response object with options data, returns response object
        """
        options = {}
        ticker = query['tick']
        ticker = ticker.lower()
        options['contracts'] = self.db.get_options_contracts(ticker)

        response.update(options)

        return response

    def HTTP_response(self, query):
        """
        Takes a dictionary object, calls for the data and returns a JSON object for the
        response for the HTTP GET Request
        """
        if query:
            values = query.keys()
            response = {}

            if 'tick' in values:
                tick = self.tick_response(response, query)
                response.update(tick)

            if 'options' in values and str(query['options']).lower() == 'true':
                option = self.options_response(response, query)
                response.update(option)

            if 'top_iv' in values and str(query['top_iv']).lower() == 'true':
                top_ivs = {}
                top_ivs['top_50'] = self.db.get_top_50('top_iv_table')
                response.update(top_ivs)

            if 'sentiment' in values and str(query['sentiment']).lower() == 'true':
                major_sentiments = {}
                major_sentiments['top_50'] = self.db.get_top_50_sentiment('market_sentiment')
                response.update(major_sentiments)

            response_json = json.dumps(response, separators=(',', ':'))

            return response_json


with HTTPServer(('', 42069), LunaOptionsHTTPServer) as server:
    server.serve_forever()
