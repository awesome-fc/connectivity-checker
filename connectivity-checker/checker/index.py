# -*- coding: utf-8 -*-

import json
import os
from time import perf_counter as pc
import socket


class Config:

    HOSTNAME = 'host'
    PORT = 'port'
    TIMEOUT = 'timeout'

    def __init__(self, event):
        self.event = event
        self.defaults = {
            self.HOSTNAME: 'baidu.com',
            self.PORT: 443,
            self.TIMEOUT: 20
        }

    def __get_property(self, property_name):
        if property_name in self.event:
            return self.event[property_name]
        if property_name in os.environ:
            return os.environ[property_name]
        if property_name in self.defaults:
            return self.defaults[property_name]
        return None

    @property
    def hostname(self):
        return self.__get_property(self.HOSTNAME)

    @property
    def port(self):
        return self.__get_property(self.PORT)

    @property
    def timeout(self):
        return self.__get_property(self.TIMEOUT)

    @property
    def reportbody(self):
        return self.__get_property(self.REPORT_RESPONSE_BODY)



class PortCheck:
    """Execution of HTTP(s) request"""

    def __init__(self, config):
        self.config = config

    def execute(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(int(self.config.timeout))
        try:
            # start the stopwatch
            t0 = pc()

            connect_result = sock.connect_ex((self.config.hostname, int(self.config.port)))
            if connect_result == 0:
                available = True
            else:
                available = False

            # stop the stopwatch
            t1 = pc()

            result = {
                'TimeTakenInMs': int((t1 - t0) * 1000),
                'Available': available
            }
            print(f"Socket connect result: {connect_result}")
            # return structure with data
            return result
        except Exception as e:
            print(f"Failed to connect to {self.config.hostname}:{self.config.port}\n{e}")
            return {'Available': False, 'Reason': str(e)}


class ResultReporter:

    def __init__(self, config):
        self.config = config
        self.options = config.cwoptions

    def report(self, result):
        if self.options['enabled'] == '1':
          pass


def event_handler(event, context):

    evt = json.loads(event)
    config = Config(evt)
    port_check = PortCheck(config)

    result = port_check.execute()

    result_json = json.dumps(result, indent=4)
    # log results
    print(f"Result of checking  {config.hostname}:{config.port}\n{result_json}")

    # return to caller
    return result

def http_handler(environ, start_response):
    context = environ['fc.context']
    request_uri = environ['fc.request_uri']
    for k, v in environ.items():
      if k.startswith('HTTP_'):
        # process custom request headers
        pass
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size) if request_body_size != 0 else b'{}'
    except (ValueError):
        request_body_size = 0
        request_body = b'{}'
    print(request_body)
    ret = event_handler(request_body, context)
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)

    result_json = json.dumps(ret, indent=4)
    return [result_json.encode('utf-8')]