"""
Abbreviations:
    CDS : Change Device State Service
"""


import sys
from utilitymodule.pylogs import PyLogs
from utilitymodule.session import Session
import microcontroller.communicator as mc_comm
import responseparser.communicator as resp_comm
from services.changedevicestate.errorhandler import SerCdsException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.info('Inside process failure method, exiting further processing')
    ser_cds_exception_obj = SerCdsException(error_source, error_type, error_msg, socket_context)
    ser_cds_exception_obj.process_exception()


class SerOneOutMsg(object):
    outputDictString = {"comm_msg": {}}

    def __init__(self):
        pass
        # print('init here in SerOneMsg')


class ChangeDeviceState(object):
    """
        This is the Core Important class of whole Module.
        Here Only Specific task will be performed according
        to given Request Message and Response Will be Routed
        to Response Parser Module
    """

    def __init__(self):
        pass
        # print('In Change Device State Constructor')

    @staticmethod
    def get_device_name(input_request):
        return input_request.comm_msg.routing_info.service_info.service_request.device_name

    @staticmethod
    def get_device_id(input_request):
        return input_request.comm_msg.routing_info.service_info.service_request.device_id

    @staticmethod
    def get_desired_device_state(input_request):
        return input_request.comm_msg.routing_info.service_info.service_request.desired_device_state

    def process(self, req_change_device_state_obj):
        print('Inside Change Device State Process')
        logg = PyLogs(__name__).get_pylogger()
        logg.info('Inside Change Device State Process')
        # input_request = None
        # input_request_id = None
        # user_info = None
        # input_message_data = None
        # output_message = None
        # socket_context = None
        # logger = None
        # noinspection PyBroadException
        user_info = req_change_device_state_obj.input_message.user_info
        input_message_data = req_change_device_state_obj.input_message.input_message_data
        output_message = req_change_device_state_obj.input_message.output_message
        socket_context = req_change_device_state_obj.input_message.socket_context
        logger = req_change_device_state_obj.input_message.logger
        # try:
        #     pass
        # except AttributeError as ser_cds_error_msg:
        #     error_source = "process method in Executor of CDS Service"
        #     error_type = ser_cds_error_msg.__class__.__name__
        #     error_msg = "AttributeError while Fetching Input Data or MetaData"
        #     process_failure(error_source, error_type, error_msg)
        # except:
        #     error_source = "process method in Executor of CDS Service"
        #     error_type = sys.exc_info()[0].__name__
        #     error_msg = "Unexpected Error while Fetching Input Data or MetaData"
        #     process_failure(error_source, error_type, error_msg)

        # print('message from Client in CDS Service:', input_message_data)

        """
            Fetch Device Id & Desired State change request from Input Request 
            and Trigger MicroController Module for further Processing
        """
        device_name = None
        device_id = None
        desired_device_state = None
        # noinspection PyBroadException
        try:
            logg.info('fetching device name, device id and requested device state from input message')
            device_name = self.get_device_name(input_message_data)
            device_id = self.get_device_id(input_message_data)
            desired_device_state = self.get_desired_device_state(input_message_data)
            logg.info(device_name + ':' + device_id + ':' + desired_device_state)
        except AttributeError as ser_CDS_error_msg:
            error_source = "process method in Executor of CDS Service"
            error_type = ser_CDS_error_msg.__class__.__name__
            error_msg = "AttributeError while Fetching Device Info"
            logg.error('Error in fetching device details, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except:
            error_source = "process method in Executor of CDS Service"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Fetching Device Info"
            logg.error('Error in fetching device details, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)

        # print('desired_device_state is : {}'.format(desired_device_state))
        # print('device_name is : {}'.format(device_name))
        # print('device_id is : {}'.format(device_id))
        '''
            Calling MicroController Module for Actual Processing
        '''
        mc_response = None
        # noinspection PyBroadException
        try:
            logg.info('Calling Micro-controller Module')
            mc_request = mc_comm.Request(device_name, device_id, desired_device_state, socket_context)
            mc_router = mc_comm.Router()
            mc_response = mc_router.execute(mc_request)
        except:
            error_source = "process method in Executor of CDS Service"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Error while MicroController Processing"
            logg.error('Error while MicroController Processing, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)

        # print(mc_response)
        logg.info(mc_response)

        """
            This mc_response is the returned response object of MicroController
            Module. it will have Resonse message Positive or Negative.
            Further Processing will be depends on Response Message
 
            Preparing Positive Response from Change Device State Module Assuming 
            MicroController Processing is successful
        """
        # new_session = None
        # noinspection PyBroadException
        try:
            logg.info('Preparing positive response after Micro-controller module processing')
            output_response = SerOneOutMsg()
            output_response.outputDictString["comm_msg"]["response_stat"] = "OK"
            print(output_response.outputDictString)

            output_message = output_response.outputDictString
            # new_session = req_change_device_state_obj
            # new_session.session.message.message_data = output_response.outputDictString
            # new_session.session.message.message_id = input_request_id
        except AttributeError as ser_CDS_error_msg:
            error_source = "process method in Executor of CDS Service"
            error_type = ser_CDS_error_msg.__class__.__name__
            error_msg = "AttributeError while Generating Service Response"
            logg.error('Error while Generating Service Response, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except:
            error_source = "process method in Executor of CDS Service"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Generating Service Response"
            logg.error('Error while Generating Service Response, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)

        # print(new_session.session.message.message_data)
        '''
            Generation Session for Response Parser Module
        '''
        logg.info('Generating session for request parser module')
        res_parser_session = Session(user_info, input_message_data, output_message, socket_context, logger)

        '''
            Calling Response Parser with Service Positive Response
        '''
        # noinspection PyBroadException
        try:
            logg.info('Calling request parser module with positive result')
            req_res_parser_obj = resp_comm.Request(res_parser_session, "OK")
            router_res_parser_obj = resp_comm.Router()
            router_res_parser_obj.execute(req_res_parser_obj)
        except:
            error_source = "process method in Executor of CDS Service"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Error while Calling Response Parser"
            logg.error('Error whie calling resonse parser, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)