import sys
from utilitymodule.pylogs import PyLogs
from services.changedevicestate.executor import ChangeDeviceState
from services.changedevicestate.errorhandler import SerCdsException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.info('Inside process failure method, exiting further processing')
    ser_cds_exception_obj = SerCdsException(error_source, error_type, error_msg, socket_context)
    ser_cds_exception_obj.process_exception()


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
    def execute(req_change_device_state_obj):
        # print('executing Router Service Change Device State')
        logg = req_change_device_state_obj.input_message.logger
        logg.info('executing Router Service Change Device State')
        err_socket_context = req_change_device_state_obj.input_message.socket_context
        # noinspection PyBroadException
        try:
            logg.info('Going to process change device state request, calling process method')
            change_device_state_obj = ChangeDeviceState()
            change_device_state_obj.process(req_change_device_state_obj)
        except:
            error_source = "excute method in Communicator of Service Change Device State"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Triggering Service Change Device State"
            logg.error('Error while Triggering Service Change Device State, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, err_socket_context, logg)


class Response(object):
    pass