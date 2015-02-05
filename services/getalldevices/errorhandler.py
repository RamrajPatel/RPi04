from utilitymodule.pylogs import PyLogs
from responseparser.communicator import Request
from responseparser.communicator import Router


class SerGadException(object):
    err_source = None
    err_type = None
    err_msg = None

    def __init__(self, err_source, err_type, err_msg, socket_context):
        self.err_msg = err_msg
        self.err_source = err_source
        self.err_type = err_type
        self.err_msg = socket_context

    def process_exception(self):
        # print('Inside process_exception method of SerGadException')
        logg = PyLogs(__name__).get_pylogger()
        logg.info('Inside process_exception method of SerGadException')
        self.trigger_response(logg)

    def trigger_response(self, logg):
        # print('Inside trigger_response method of SerGadException')
        logg.info('Inside trigger_response method of SerGadException')
        req_res_parser_obj = Request(self, "ERROR")
        router_res_parser_obj = Router()
        router_res_parser_obj.execute(req_res_parser_obj)