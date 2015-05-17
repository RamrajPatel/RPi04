from utilitymodule.pylogs import PyLogs
from responseparser.executor import BasicResponseParser


class InputMessage(object):
    user_info = None
    input_message_data = None
    output_message = None
    socket_context = None
    logger = None

    def __init__(self, session_data):
        self.user_info = session_data.user_info
        self.input_message_data = session_data.input_message
        self.output_message = session_data.output_message
        self.socket_context = session_data.socket_context
        self.logger = PyLogs(__name__).get_pylogger()
        # self.logger = session_data.logger


class Request:
    input_message = None
    status = None

    def __init__(self, input_message, status):
        self.input_message = input_message
        self.status = status


class Router(object):
    def __init__(self):
        pass

    @staticmethod
    def execute(req_res_parser_obj):
        # print('exec Router Response parser')
        logg = req_res_parser_obj.input_message.logger
        logg.info('exec Router Response parser, calling parse for response processing')
        resp_parser_exec_obj = BasicResponseParser()
        resp_parser_exec_obj.parse(req_res_parser_obj)


class Response(object):
    pass