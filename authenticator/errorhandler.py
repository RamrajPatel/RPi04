from utilitymodule.pylogs import PyLogs
from responseparser.communicator import Request
from responseparser.communicator import Router


class AuthenticatorException(object):
    err_source = None
    err_type = None
    err_msg = None
    socket_context = None

    def __init__(self, err_source, err_type, err_msg, socket_context):
        self.err_msg = err_msg
        self.err_source = err_source
        self.err_type = err_type
        self.socket_context = socket_context

    def process_exception(self):
        logg = PyLogs(__name__).get_pylogger()
        logg.error('Inside process_exception method of AuthenticatorException')
        # print('Inside process_exception method of AuthenticatorException')
        self.trigger_response()

    def trigger_response(self):
        logg.error('Inside trigger_response method of AuthenticatorException')
        # print('Inside trigger_response method of AuthenticatorException')
        req_res_parser_obj = Request(self, "ERROR")
        router_res_parser_obj = Router()
        router_res_parser_obj.execute(req_res_parser_obj)