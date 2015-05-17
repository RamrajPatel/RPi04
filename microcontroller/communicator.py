import sys
from utilitymodule.pylogs import PyLogs
from microcontroller.executor import MicrocontrollerInterface
from microcontroller.errorhandler import MicroControllerException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.info('Inside process failure method, exiting further processing')
    mc_exception_obj = MicroControllerException(error_source, error_type, error_msg, socket_context)
    mc_exception_obj.process_exception()


class Request:
    def __init__(self, device_name, device_id, desired_device_state, socket_context):
        self.device_name = device_name
        self.device_id = device_id
        self.desired_device_state = desired_device_state
        self.socket_context = socket_context
        self.logger = PyLogs(__name__).get_pylogger()


class Router(object):
    def __init__(self):
        pass

    @staticmethod
    def execute(mc_request):
        """
            Here Response Object Has been Passed to executor Module so that it can have
            Return Response of that Module and can be returned back to Service Module.
            Since Communicator is importing Executor MicrocontrollerInterface Class
            and we have to use Response in same class in executor So Communicator can't
            be imported there. That's why it is being passed at time of Calling
            process() itself.
        """
        # print('executing MicroController Router execute function')
        logg = mc_request.logger
        logg.info('Inside execute method')

        socket_context = mc_request.socket_context
        # noinspection PyBroadException
        try:
            logg.info('Going to process change device request in Micro-Controller')
            mc_interface = MicrocontrollerInterface()
            resp_obj = Response()
            mc_response = mc_interface.process(mc_request, resp_obj)
        except:
            error_source = "execute method in Communicator of MicroController"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Triggering MicroController executor"
            logg.error('Error while Triggering MicroController executor, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        return mc_response


class Response(object):
    def __init__(self):
        pass