import sys
from globals import GlobalData
from utilitymodule.pylogs import PyLogs
from utilitymodule.session import Session
import services.getalldevices.communicator as gad_comm
import services.changedevicestate.communicator as cds_comm
from requestrouter.errorhandler import ReqRouterException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.error('Inside process failure method, exiting further processing')
    req_router_exception_obj = ReqRouterException(error_source, error_type, error_msg, socket_context)
    req_router_exception_obj.process_exception()


class BasicRequestRouter(object):
    def __init__(self):
        print('Inside Constructor of BasicRequestRouter')

    def route(self, req_router_request_obj):
        # print('Inside Request Router route method')
        logg = PyLogs(__name__).get_pylogger()
        logg.info('Inside route method')
        self.identify_and_call_service(req_router_request_obj, logg)

    @staticmethod
    def get_service_name(req_router_request_obj):
        return req_router_request_obj.input_message.input_message_data.comm_msg.routing_info.service_info.service_name

    @staticmethod
    def initiate_getalldevice_service(req_router_session):
        ser_gad_msg = gad_comm.InputMessage(req_router_session)
        req_getalldevice_msg_obj = gad_comm.Request(ser_gad_msg)
        router_getalldevice_obj = gad_comm.Router()
        router_getalldevice_obj.execute(req_getalldevice_msg_obj)

    @staticmethod
    def initiate_changedevicestate_service(req_router_session):
        ser_cds_msg = cds_comm.InputMessage(req_router_session)
        req_getalldevice_msg_obj = cds_comm.Request(ser_cds_msg)
        router_getalldevice_obj = cds_comm.Router()
        router_getalldevice_obj.execute(req_getalldevice_msg_obj)

    # noinspection PyBroadException
    def identify_and_call_service(self, req_router_request_obj, logg):
        req_service_name = None
        # socket_context = req_router_request_obj.input_message.socket_context
        '''
            Getting Session input objects
        '''
        logg.info('Generating session')
        user_info = req_router_request_obj.input_message.user_info
        input_message_data = req_router_request_obj.input_message.input_message_data
        output_message = req_router_request_obj.input_message.output_message
        socket_context = req_router_request_obj.input_message.socket_context
        logger = req_router_request_obj.input_message.logger

        # noinspection PyBroadException
        '''
            Fetching Service name from input message
        '''
        try:
            req_service_name = self.get_service_name(req_router_request_obj)
            logg.info('service name from input request is: ' + req_service_name)
        except AttributeError as req_router_error_msg:
            error_source = "identify_and_call_service method in Executor of RequestRouter"
            error_type = req_router_error_msg.__class__.__name__
            error_msg = "AttributeError while fetching Service name from Input Request"
            logg.error('Error while fetching service name, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except:
            error_source = "identify_and_call_service method in Executor of RequestRouter"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while fetching service name"
            logg.error('Error while fetching service name, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)

        '''
            Creation Session Object for next module(Request Router)
        '''
        logg.info('Generating session for service')
        req_router_session = Session(user_info, input_message_data, output_message, socket_context, logger)

        '''
            Deciding service to be initiated to process input request
        '''
        logg.info('Calling corresponding service')
        if req_service_name == GlobalData.SERVIE_GET_ALL_DEVICES:
            print('calling get all device service')
            # noinspection PyBroadException
            try:
                self.initiate_getalldevice_service(req_router_session)
            except:
                error_source = "identify_and_call_service method in Executor of RequestRouter"
                error_type = sys.exc_info()[0].__name__
                error_msg = "Unexpected Error while initiating get all device request"
                process_failure(error_source, error_type, error_msg, socket_context, logg)

        elif req_service_name == GlobalData.SERVICE_CHANGE_DEVICE_STATE:
            print('calling change device state services')
            # noinspection PyBroadException
            try:
                self.initiate_changedevicestate_service(req_router_session)
            except:
                error_source = "initiate_changedevicestate_service method in Executor of RequestRouter"
                error_type = sys.exc_info()[0].__name__
                error_msg = "Unexpected Error while initiating change device state request"
                process_failure(error_source, error_type, error_msg, socket_context, logg)
        else:
            print('Invalid Service Request')
            ''' Raise Error For Invalid Service Request'''