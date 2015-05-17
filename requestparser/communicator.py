from sys import exc_info
from utilitymodule.pylogs import PyLogs
from requestparser.executor import BasicRequestParser
from requestparser.errorhandler import ReqParserException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.error('Inside process_failure method, exiting program')
    req_parser_exception_obj = ReqParserException(error_source, error_type, error_msg, socket_context)
    req_parser_exception_obj.process_exception()


class InputMessage(object):
    """
        This Class will store Input Client Request Message
        and Other Meta Data like Dispatcher ID and socket Context
    """
    dispatcher_id = None
    user_info = None
    input_message_bytes = None
    output_message = None
    socket_context = None
    logger = None

    def __init__(self, dispatcher_id, input_message_bytes):
        self.dispatcher_id = dispatcher_id
        self.user_info = input_message_bytes.user_info
        self.input_message_bytes = input_message_bytes.input_message
        self.output_message = input_message_bytes.output_message
        self.socket_context = input_message_bytes.socket_context
        self.logger = PyLogs(__name__).get_pylogger()
        # my_logger = PyLogs(__name__)
        # logg = my_logger.get_pylogger()


class Request(object):
    input_message = None

    def __init__(self, input_message):
        self.input_message = input_message


class Response(object):
    pass


class Router(object):
    def __init__(self):
        pass

    @staticmethod
    def execute(input_request):
        logg = input_request.input_message.logger
        logg.info('Inside Router execute Method')

        # err_socket_context = None
        err_socket_context = input_request.input_message.socket_context
        # noinspection PyBroadException
        try:
            logg.info('Calling executor for parsing the input request')
            req_parse_exe_obj = BasicRequestParser()
            req_parse_exe_obj.parse(input_request)
        except:
            error_source = "execute method in Communicator of RequestParser"
            error_type = exc_info()[0].__name__
            error_msg = "Unexpected Error while Triggering Request Parser executor"
            logg.error('Unexpected Error while Triggering Request Parser executor, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, err_socket_context, logg)