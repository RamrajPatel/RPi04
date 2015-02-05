import sys
from utilitymodule.pylogs import PyLogs
from services.getalldevices.executor import GetAllDevices
from services.getalldevices.errorhandler import SerGadException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.error('Inside process failure method, exiting further processing')
    ser_gad_exception_obj = SerGadException(error_source, error_type, error_msg, socket_context)
    ser_gad_exception_obj.process_exception()


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

    def __init__(self, input_message):
        self.input_message = input_message


class Router(object):
    def __init__(self):
        pass

    @staticmethod
    def execute(req_getalldevice_msg_obj):
        # print('executing Router Get All Devices List')
        logg = req_getalldevice_msg_obj.input_message.logger
        logg.info('executing Router Get All Devices List')

        err_socket_context = req_getalldevice_msg_obj.input_message.socket_context
        # noinspection PyBroadException
        try:
            logg.info('Calling executor for processing request')
            getalldevices_obj = GetAllDevices()
            getalldevices_obj.process(req_getalldevice_msg_obj)
        except:
            error_source = "excute method in Communicator of Service GAD"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Triggering Service GAD"
            logg.info('Error while Triggering Service GAD, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, err_socket_context, logg)


class Response(object):
    pass