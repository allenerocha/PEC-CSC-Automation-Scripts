import urllib.request
import json
from os import path


def _retrieve_data(endpoint: str) -> object:
    error_codes = {
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found (Previously "Moved temporarily")',
        303: 'See Other (since HTTP/1.1)',
        304: 'Not Modified (RFC 7232)',
        305: 'Use Proxy (since HTTP/1.1)',
        306: 'Switch Proxy',
        307: 'Temporary Redirect (since HTTP/1.1)',
        308: 'Permanent Redirect (RFC 7538)',
        400: 'Bad Request',
        401: 'Unauthorized (RFC 7235)',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required (RFC 7235)',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed (RFC 7232)',
        413: 'Payload Too Large (RFC 7231)',
        414: 'URI Too Long (RFC 7231)',
        415: 'Unsupported Media Type (RFC 7231)',
        416: 'Range Not Satisfiable (RFC 7233)',
        417: 'Expectation Failed',
        418: "I'm a teapot (RFC 2324, RFC 7168)",
        421: 'Misdirected Request (RFC 7540)',
        422: 'Unprocessable Entity (WebDAV; RFC 4918)',
        423: 'Locked (WebDAV; RFC 4918)',
        424: 'Failed Dependency (WebDAV; RFC 4918)',
        425: 'Too Early (RFC 8470)',
        426: 'Upgrade Required',
        428: 'Precondition Required (RFC 6585)',
        429: 'Too Many Requests (RFC 6585)',
        431: 'Request Header Fields Too Large (RFC 6585)',
        451: 'Unavailable For Legal Reasons (RFC 7725)',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not',
        506: 'Variant Also Negotiates (RFC 2295)',
        507: 'Insufficient Storage (WebDAV; RFC 4918)',
        508: 'Loop Detected (WebDAV; RFC 5842)',
        510: 'Not Extended (RFC 2774)',
        511: 'Network Authentication Required (RFC 6585)'
    }
    url_data = urllib.request.urlopen(endpoint)
    if url_data.getcode() >= 300:
        raise Exception(
            'Unsuccessful connection to the OpenWeatherAPI server.\nError code: {}.\n{}'.format(url_data.getcode,
                                                                                                error_codes[
                                                                                                    url_data.getcode]))
    return json.loads(url_data.read())


class current_weather:
    def __init__(self, api_code: int, *args: str) -> None:
        """
        By city name
        http://api.openweathermap.org/data/2.5/weather?q={city name}&appid={KEY}                                                                           -   CODE 0

        http://api.openweathermap.org/data/2.5/weather?q={city name},{country code}&appid={KEY}                                                            -   CODE 1

        By city ID
        http://api.openweathermap.org/data/2.5/weather?id={id}&appid={KEY}                                                                                 -   CODE 2

        By geographic coordinates
        http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={KEY}                                                                     -   CODE 3

        By ZIP code
        http://api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={KEY}                                                           -   CODE 4

        Cities in cycle
        http://api.openweathermap.org/data/2.5/find?lat={lat}&lon={lon}&cnt={number of cities around the point that should be returned}&appid={KEY}        -   CODE 5

        Call for several city IDs
        http://api.openweathermap.org/data/2.5/group?id={id1},{id2},...,{id19},{id20}&units=metric&appid={KEY}                                             -   CODE 6

        :param api_code: request desired
        :param args: parameters for the request
        """
        # check code
        if api_code not in range(8):
            raise ValueError('API code must be between [0,7].\nView documentation for more information.')

        if not path.isfile('OpenWeatherAPI.key'):
            raise FileExistsError('API key must be in OpenWeatherAPI directory.')

        self.api_code = api_code
        self.args = list()
        self.api_key = str()
        with open('OpenWeatherAPI.key', 'r') as key_file:
            self.api_key = key_file.readline()
        self.json_data = object()
        for argument in args:
            self.args.append(argument)

        if self.api_code == 0 or self.api_code == 1:
            self.json_data = self._city_request(self.api_code, self.args)

        elif self.api_code == 2:
            self.json_data = self._id_request(self.api_code, self.args)

        elif self.api_code == 3:
            self.json_data = self._geo_request(self.api_code, self.args)

        elif self.api_code == 4:
            self.json_data = self._zip_request(self.api_code, self.args)

        elif self.api_code == 5:
            self.json_data = self._cycle_request(self.api_code, self.args)

        elif self.api_code == 6:
            self.json_data = self._multi_city_request(self.api_code, self.args)

        print(self.json_data)

    def _city_request(self, api_code: int, args: list) -> object:
        """
        formats the endpoint based on api_code and the arguments
        :param api_code: which endpoint to use
        :param args: arguments for the endpoint
        :return: json object retrieved from the endpoint
        """
        if api_code == 0:
            if len(args) != 1:
                raise IndexError(
                    'Not the correct amount of values for api code {}.\nExpected 1 received {}.'.format(api_code,
                                                                                                        len(args)))
            endpoint = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(args[0], self.api_key)
        else:
            if len(args) != 2:
                raise IndexError(
                    'Not the correct amount of values for api code {}.\nExpected 2 received {}.'.format(api_code,
                                                                                                        len(args)))
            endpoint = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}'.format(args[0], args[1],
                                                                                                self.api_key)
        return _retrieve_data(endpoint)

    def _id_request(self, api_code: int, args: list) -> object:
        if len(args) != 1:
            raise IndexError(
                'Not the correct amount of values for api code {}.\nExpected 1 received {}.'.format(api_code,
                                                                                                    len(args)))
        endpoint = 'http://api.openweathermap.org/data/2.5/weather?id={}&appid={}'.format(args[0], self.api_key)
        return _retrieve_data(endpoint)

    def _geo_request(self, api_code: int, args: list) -> object:
        if len(args) != 2:
            raise IndexError(
                'Not the correct amount of values for api code {}.\nExpected 2 received {}.'.format(api_code,
                                                                                                    len(args)))
        endpoint = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(args[0], args[1],
                                                                                                  self.api_key)
        return _retrieve_data(endpoint)

    def _zip_request(self, api_code: int, args: list) -> object:
        if len(args) != 2:
            raise IndexError(
                'Not the correct amount of values for api code {}.\nExpected 2 received {}.'.format(api_code,
                                                                                                    len(args)))
        endpoint = 'http://api.openweathermap.org/data/2.5/weather?zip={},{}&appid={}'.format(args[0], args[1],
                                                                                              self.api_key)
        return _retrieve_data(endpoint)

    def _cycle_request(self, api_code: int, args: list) -> object:
        if len(args) != 3:
            raise IndexError(
                'Not the correct amount of values for api code {}.\nExpected 3 received {}.'.format(api_code,
                                                                                                    len(args)))
        endpoint = 'http://api.openweathermap.org/data/2.5/find?lat={}&lon={}&cnt={}&appid={}'.format(args[0], args[1],
                                                                                                      args[2],
                                                                                                      self.api_key)
        return _retrieve_data(endpoint)

    def _multi_city_request(self, api_code: int, args: list) -> object:
        if len(args) < 1:
            raise IndexError(
                'Not the correct amount of values for api code {}.\nExpected at least 1 received {}.'.format(api_code,
                                                                                                             len(args)))
        locations = str()
        for index in range(len(args)):
            if index != (len(args) - 1):
                locations += args[index] + ','
            else:
                locations += args[index]
        endpoint = 'http://api.openweathermap.org/data/2.5/group?id={}&units=metric&appid={}'.format(locations,
                                                                                                     self.api_key)
        return _retrieve_data(endpoint)


# test1 = current_weather(1, 'chicago', 'us')
# test2 = current_weather(2, '4887398')
# test3 = current_weather(3, '41.850029', '-87.650047')
# test4 = current_weather(4, '60046', 'us')
# test5 = current_weather(5, '41.950029', '-87.750047', '3')
# test6 = current_weather(6, '4887398', '4888892', '4889107')
