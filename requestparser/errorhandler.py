from utilitymodule.pylogs import PyLogs
from responseparser.communicator import Request
from responseparser.communicator import Router


class ReqParserException(object):
    err_source = ""
    err_type = ""
    err_msg = ""
    socket_context = ""

    def __init__(self, err_source, err_type, err_msg, socket_context):
        self.err_msg = err_msg
        self.err_source = err_source
        self.err_type = err_type
        self.socket_context = socket_context

    def process_exception(self):
        # print('Inside process_exception method of ReqParserException')
        logg = PyLogs(__name__).get_pylogger()
        logg.error('Inside process_exception method of ReqParserException')
        self.trigger_response(logg)

    def trigger_response(self, logg):
        # print('Inside trigger_response method of ReqParserException')
        logg.error('Inside trigger_response method of ReqParserException')
        req_res_parser_obj = Request(self, "ERROR")
        router_res_parser_obj = Router()
        router_res_parser_obj.execute(req_res_parser_obj)