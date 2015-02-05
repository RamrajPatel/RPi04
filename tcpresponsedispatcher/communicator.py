import sys
import socket
from utilitymodule.pylogs import PyLogs
from tcpresponsedispatcher.executor import BasicTcpResponseDispatcher


class OutputMessage(object):
    user_info = None
    input_message_data = None
    output_message = None
    socket_context = None
    logger = None

    def __init__(self, session_data):
        self.user_info = session_data.user_info
        self.input_message = session_data.input_message
        self.output_message = session_data.output_message
        self.socket_context = session_data.socket_context
        self.logger = PyLogs(__name__).get_pylogger()
        # self.logger = session_data.logger


class Request(object):
    output_response = None
    
    def __init__(self, output_response):
        self.output_response = output_response


class Response(object):
    pass


class Router(object):
    def __init__(self):
        pass
    
    @staticmethod
    def execute(req_tcp_res_disp_obj):
        # print('executing Router Response Dispatcher')
        logg = req_tcp_res_disp_obj.output_response.logger
        logg.info('executing Router Response Dispatcher')
        try:
            rd = BasicTcpResponseDispatcher()
            rd.send_reply(req_tcp_res_disp_obj)
        except (AttributeError, TypeError, socket.error) as err_message:
            print('In execute method of response Dispatcher Communicator')
            print('Data sending Failed, Reason:', err_message)
            logg.error('Error while sending data, Reason:' + err_message)
            sys.exit()