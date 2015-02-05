import sys
from utilitymodule.pylogs import PyLogs
from authenticator.executor import BasicAuthenticator
from authenticator.errorhandler import AuthenticatorException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.error('Inside process failure method, Exiting further processing')
    authenticator_exception_obj = AuthenticatorException(error_source, error_type, error_msg, socket_context)
    authenticator_exception_obj.process_exception()


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
    def execute(auth_req_obj):
        logg = auth_req_obj.input_message.logger
        logg.info('Inside execute method')
        err_socket_context = auth_req_obj.input_message.socket_context
        # noinspection PyBroadException
        try:
            logg.info('Calling Basic Authenticator')
            auth_exec_obj = BasicAuthenticator()
            auth_exec_obj.authenticate(auth_req_obj)
        except:
            error_source = "excute method in Communicator of Authenticator"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Triggering Authenticator executor"
            logg.error('Error while triggering Basic Authenticator, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, err_socket_context, logg)