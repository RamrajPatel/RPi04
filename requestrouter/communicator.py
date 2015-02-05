import sys
from utilitymodule.pylogs import PyLogs
from requestrouter.executor import BasicRequestRouter
from requestrouter.errorhandler import ReqRouterException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.error('Inside process_failure method, exiting further processing')
    req_router_exception_obj = ReqRouterException(error_source, error_type, error_msg, socket_context)
    req_router_exception_obj.process_exception()


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
    def execute(req_router_request_obj):
        # print('Inside execute method of Router Class in Request Router')
        logg = req_router_request_obj.input_message.logger
        logg.info('Inside execute method of Router')

        err_socket_context = req_router_request_obj.input_message.socket_context
        # noinspection PyBroadException
        try:
            logg.info('Calling route method')
            router_exec_obj = BasicRequestRouter()
            router_exec_obj.route(req_router_request_obj)
        except:
            error_source = "excute method in Communicator of RequestRouter"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Triggering Request Router executor"
            logg.error('Error while triggering route method, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, err_socket_context, logg)