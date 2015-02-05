from utilitymodule.pylogs import PyLogs
from responseparser.communicator import Request
from responseparser.communicator import Router


class MicroControllerException(object):
    err_msg = None
    err_source = None
    err_type = None
    socket_context = None

    def __init__(self, err_source, err_type, err_msg, socket_context):
        self.err_msg = err_msg
        self.err_source = err_source
        self.err_type = err_type
        self.socket_context = socket_context

    def process_exception(self):
        # print('Inside process_exception method of MicroControllerException')
        logg = PyLogs(__name__).get_pylogger()
        logg.info('Inside process_exception method of MicroControllerException')
        self.trigger_response(logg)

    def trigger_response(self, logg):
        # print('Inside trigger_response method of MicroControllerException')
        logg.info('Inside trigger_response method of MicroControllerException')
        req_res_parser_obj = Request(self, "ERROR")
        router_res_parser_obj = Router()
        router_res_parser_obj.execute(req_res_parser_obj)