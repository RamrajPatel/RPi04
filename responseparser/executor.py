import sys
from utilitymodule.pylogs import PyLogs
from utilitymodule import loadparamfile
from utilitymodule.session import Session
from tcpresponsedispatcher.communicator import Router
from tcpresponsedispatcher.communicator import Request
from tcpresponsedispatcher.communicator import OutputMessage

outputDictString = {"comm_msg": {}}


class Encoder(object):
    """
        This class will convert Output Python Object into JSON Response
    """

    encode_output_message = None

    def __init__(self):
        print('Inside Encoder Class')

    @staticmethod
    def encode_pyobject(response_message):
        encode_output_message = loadparamfile.json.dumps(response_message, default=lambda o: o.__dict__, indent=4,
                                                         sort_keys=True)
        print(encode_output_message)
        return encode_output_message


class BasicResponseParser(object):
    def __init__(self):
        print('In BasicResponseParser Constructor')

    @staticmethod
    def get_error_params_file_name():
        return loadparamfile.GlobalData.ERROR_PARAMS_FNAME

    @staticmethod
    def get_error_details(error_type, ref_erm_param):
        if error_type in ref_erm_param["file_data"]:
            error_code = ref_erm_param["file_data"][error_type]["error_code"]
            error_description = ref_erm_param["file_data"][error_type]["error_description"]
            error_exit_flag = ref_erm_param["file_data"][error_type]["error_action_flag"]
        else:
            if "DEFAULT_ERROR" in ref_erm_param["file_data"]:
                error_code = ref_erm_param["file_data"][error_type]["error_code"]
                error_description = ref_erm_param["file_data"][error_type]["error_description"]
                error_exit_flag = ref_erm_param["file_data"][error_type]["error_action_flag"]
            else:
                print('Error Parameter in error param file not found')
                error_code = 155
                error_description = "Unexpected error encounter, please contact system team"
                # error_exit_flag = "EXIT"
                error_exit_flag = "SHOW"
        return error_code, error_description, error_exit_flag

    def process_error(self, req_res_parser_obj, logg):
        # print('Inside process_error in Response Parser')
        logg.info('Inside process_error in Response Parser')
        '''
            Load Error Parameters
        '''
        # erm_param_file = None
        ref_erm_param = None
        # noinspection PyBroadException
        try:
            erm_param_file = self.get_error_params_file_name()
            # print('error param file name is:', erm_param_file)
            logg.info('error param file name is:' + erm_param_file)
            ref_erm_param = loadparamfile.LoadParamsFile(erm_param_file)
        except:
            logg.error('Unexpected error encountered while loading error param file, exiting program')
            # print('Unexpected error encountered while loading error param file, exiting program')
            # sys.exit()
            # error_code = 155
            # error_description = "Unexpected error encounter, please contact system team"
            # error_exit_flag = "SHOW"

        print(ref_erm_param)

        print('Error Message: {}'.format(req_res_parser_obj.error_msg))
        print('Error Type: {}'.format(req_res_parser_obj.error_type))
        print('Error Source: {}'.format(req_res_parser_obj.error_source))

        error_type = req_res_parser_obj.error_type

        '''
            Get Error Details
        '''
        error_code, error_description, error_exit_flag = self.get_error_details(error_type, ref_erm_param)

        print('Error Code: ', error_code)
        print('Error Description: ', error_description)
        print('Error Exit Flag: ', error_exit_flag)

        '''
            If Error can not be sent to Front-End Server then do Exit here
            Otherwise Generate Response for Output Data
            Also load ERMPARAM file to load error codes and other details
        '''
        if error_exit_flag == "EXIT":
            print('Encountered System Error, Exiting Program, Error Code: {} and Error Description : {}', error_code,
                  error_description)
            sys.exit()
        else:
            '''
                Preparing Error Response For Given Request
            '''
            print('Generating Error Response')
            outputDictString["comm_msg"]["response_stat"] = "ERROR"
            outputDictString["comm_msg"]["error_info"]["error_code"] = error_code

            if req_res_parser_obj.error_msg and not req_res_parser_obj.error_msg.isspace():
                outputDictString["comm_msg"]["error_info"]["error_msg"] = req_res_parser_obj.error_msg
            else:
                outputDictString["comm_msg"]["error_info"]["error_msg"] = error_description

            outputDictString["comm_msg"]["error_info"]["error_type"] = req_res_parser_obj.error_type
            outputDictString["comm _msg"]["error_info"]["error_source"] = req_res_parser_obj.error_source

            return outputDictString

    def parse(self, req_res_parser_obj):
        # print('In Parse method of BasicResponseParser Class')
        logg = PyLogs(__name__).get_pylogger()
        logg.info('In Parse method of BasicResponseParser Class')

        user_info = None
        input_request = None
        # response_message = None
        # socket_context = None
        logger = None

        if req_res_parser_obj.status == "ERROR":
            # print('Response is having error, processing error response')
            logg.info('Response is having error, processing error response')
            response_message = self.process_error(req_res_parser_obj, logg)
            socket_context = req_res_parser_obj.socket_context
        else:
            # print('Successful request processing, in response parser for response parsing')
            logg.info('Successful request processing, in response parser for response parsing')
            user_info = req_res_parser_obj.input_message.user_info
            input_request = req_res_parser_obj.input_message.input_message
            response_message = req_res_parser_obj.input_message.output_message
            socket_context = req_res_parser_obj.input_message.socket_context
            logger = req_res_parser_obj.input_message.logger

        # print('Connection details are as: ', socket_context)

        # ''' Fetching Socket Context From Globally Maintained List '''
        # # socketcontext = loadparamfile.GlobalData.store_socket[1]
        # socketcontext = loadparamfile.GlobalData.store_socket[message_id]

        '''
            Prepare your Response Object and Pass it to the given below
            mention Object for time being it is Decoded Request Object
        '''
        # print('Encoding JSON String into Request Parser')
        logg.info('Encoding JSON String into Request Parser')
        encoded_output_message = Encoder().encode_pyobject(response_message)
        print(encoded_output_message)

        '''
            Encoding Back the Message in Bytes
        '''
        message_bytes = bytes(encoded_output_message, 'UTF-8')

        '''
            Preparing Session object for response dispatcher
        '''
        res_dispatcher_session = Session(user_info, input_request, message_bytes, socket_context, logger)

        # output_message = OutputMessage(socket_context, message_bytes)
        output_message = OutputMessage(res_dispatcher_session)
        req_tcp_res_disp_obj = Request(output_message)
        router_tcp_res_disp_obj = Router()
        router_tcp_res_disp_obj.execute(req_tcp_res_disp_obj)
