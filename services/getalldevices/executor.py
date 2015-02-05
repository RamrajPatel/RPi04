"""
Abbreviations:
    GAD : Get All Devices
"""

import sys
import json
from globals import GlobalData
from utilitymodule.pylogs import PyLogs
from utilitymodule.session import Session
from responseparser.communicator import Request
from responseparser.communicator import Router
from services.getalldevices.errorhandler import SerGadException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.error('Inside process failure method, exiting further processing')
    ser_gad_exception_obj = SerGadException(error_source, error_type, error_msg, socket_context)
    ser_gad_exception_obj.process_exception()


class SerOneOutMsg(object):
    outputDictString = {"comm_msg": {}}

    def __init__(self):
        print('init here in SerOneMsg')


class GetAllDevices(object):
    def __init__(self):
        pass

    @staticmethod
    def get_all_devices():
        json_data = open(GlobalData.GET_ALL_DEVICE_LIST_FNAME).read()
        return json.loads(json_data)

    def process(self, req_getalldevice_msg_obj):
        # print('in GetAllDevices Process')
        # logg = req_getalldevice_msg_obj.input_message.logger
        logg = PyLogs(__name__).get_pylogger()
        logg.info('Inside GetAllDevices Process method')
        # user_info = None
        # input_message_data = None
        # output_message = None
        # socket_context = None
        # logger = None
        # noinspection PyBroadException
        # try:
        user_info = req_getalldevice_msg_obj.input_message.user_info
        input_message_data = req_getalldevice_msg_obj.input_message.input_message_data
        output_message = req_getalldevice_msg_obj.input_message.output_message
        socket_context = req_getalldevice_msg_obj.input_message.socket_context
        logger = req_getalldevice_msg_obj.input_message.logger
        # except AttributeError as ser_gad_error_msg:
        #     error_source = "process method in Executor of GAD Service"
        #     error_type = ser_gad_error_msg.__class__.__name__
        #     error_msg = "AttributeError while Fetching Input Data or MetaData"
        #     process_failure(error_source, error_type, error_msg)
        # except:
        #     error_source = "process method in Executor of GAD Service"
        #     error_type = sys.exc_info()[0].__name__
        #     error_msg = "Unexpected Error while Fetching Input Data or MetaData"
        #     process_failure(error_source, error_type, error_msg)

        # print('message from Client in Service:', input_message_data)
        logg.info('message from Client in Service:' + input_message_data)

        '''
            Fetching All Devices from All Device Details Params file
        '''
        output_response = SerOneOutMsg()
        devices_details = None
        # noinspection PyBroadException
        try:
            logg.info('Calling get all device method')
            devices_details = self.get_all_devices()
        except ValueError as ser_gad_error_msg:
            error_source = "process method in Executor of GAD Service"
            error_type = ser_gad_error_msg.__class__.__name__
            error_msg = "ValueError, params file load error"
            logg.error('Param file load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except TypeError as ser_gad_error_msg:
            error_source = "process method in Executor of GAD Service"
            error_type = ser_gad_error_msg.__class__.__name__
            error_msg = "TypeError, param file load error"
            logg.error('Param file load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except EOFError as ser_gad_error_msg:
            error_source = "process method in Executor of GAD Service"
            error_type = ser_gad_error_msg.__class__.__name__
            error_msg = "EOFError, params file is empty"
            logg.error('Param file load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except IOError as ser_gad_error_msg:
            error_source = "process method in Executor of GAD Service"
            error_type = ser_gad_error_msg.__class__.__name__
            error_msg = "IOError, loding param file error"
            logg.error('Param file load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except AttributeError as ser_gad_error_msg:
            error_source = "process method in Executor of GAD Service"
            error_type = ser_gad_error_msg.__class__.__name__
            error_msg = "AttributeError while Fetching Input Data or MetaData"
            logg.error('Param file load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except:
            error_source = "process method in Executor of GAD Service"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Fetching Input Data or MetaData"
            logg.error('Param file load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)

        logg.info(devices_details["home_info"])
        # print(devices_details["home_info"])

        '''
            Generating Response for Service Get All Devices
        '''
        # new_session = None
        # noinspection PyBroadException
        try:
            output_response.outputDictString["comm_msg"]["response_stat"] = "OK"
            output_response.outputDictString["comm_msg"]["home_info"] = devices_details["home_info"]
            # print(output_response.outputDictString)
            logg.info(output_response.outputDictString)
            output_message = output_response.outputDictString
        except AttributeError as ser_gad_error_msg:
            error_source = "process method in Executor of GAD Service"
            error_type = ser_gad_error_msg.__class__.__name__
            error_msg = "AttributeError while Generating Service Response"
            logg.error('Error while generating service response, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except:
            error_source = "process method in Executor of GAD Service"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Generating Service Response"
            logg.error('Error while generating service response, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)

        print(output_message)
        logg.info(output_message)
        '''
            Generation Session for Response Parser Module
        '''
        res_parser_session = Session(user_info, input_message_data, output_message, socket_context, logger)

        '''
            Calling Response Parser with Positive Service response
        '''
        # noinspection PyBroadException
        try:
            # req_res_parser_obj = Request(new_session, "OK")
            logg.info('Calling response parser for sending outputs')
            req_res_parser_obj = Request(res_parser_session, "OK")
            router_res_parser_obj = Router()
            router_res_parser_obj.execute(req_res_parser_obj)
        except:
            error_source = "process method in Executor of GAD Service"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Error while Calling Response Parser"
            logg.error('Error while Calling Response Parser, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)