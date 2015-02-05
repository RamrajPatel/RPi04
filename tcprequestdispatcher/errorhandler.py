# from pickle import NONE
from responseparser.communicator import Request
from responseparser.communicator import Router


class ReqDispatcherException(object):
    err_source = None
    err_type = None
    err_msg = None
    socket_context = None
    # error_code=0

    def __init__(self, err_source, err_type, err_msg, socket_context):
        # self.error_code=error_code
        self.err_msg = err_msg
        self.err_source = err_source
        self.err_type = err_type
        self.socket_context = socket_context

    def process_exception(self):
        print('Inside process_exception method of ReqDispatcherException')
        self.trigger_response()

    def trigger_response(self):
        print('Inside trigger_response method of ReqDispatcherException')
        req_res_parser_obj = Request(self, "ERROR")
        router_res_parser_obj = Router()
        router_res_parser_obj.execute(req_res_parser_obj)