import sys
import json
from collections import namedtuple
from utilitymodule.pylogs import PyLogs
from authenticator.communicator import Router
from authenticator.communicator import Request
from authenticator.communicator import InputMessage
from utilitymodule.session import Session
from requestparser.errorhandler import ReqParserException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.info('Inside process_failure method, Exiting Program')
    req_parser_exception_obj = ReqParserException(error_source, error_type, error_msg, socket_context)
    req_parser_exception_obj.process_exception()


class Decoder(object):
    """
        This class will convert Input JSON Request into Python Object
    """

    decode_input_message = None

    def __init__(self):
        print('Inside Decoder Class')

    def decode_json(self, input_request, socket_context, logg):
        # noinspection PyBroadException
        logg.info('Inside decode_json method')
        decode_input_message = None
        # socket_context = input_request.input_message.socket_context
        # noinspection PyBroadException
        try:
            logg.info('Decoding Input Request')
            decode_input_message = json.loads(input_request, object_hook=self._json_object_hook)
        except ValueError as req_parse_error_msg:
            error_source = "decode_json method in Executor of RequestParser"
            error_type = req_parse_error_msg.__class__.__name__
            error_msg = "ValueError in decoding JSON, Please Contact with Support Team"
            logg.error('Decoding Input Request Error' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except AttributeError as req_parse_error_msg:
            error_source = "decode_json method in Executor of RequestParser"
            error_type = req_parse_error_msg.__class__.__name__
            error_msg = "AttributeError in decoding JSON, Please Contact with Support Team"
            logg.error('Decoding Input Request Error' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except:
            error_source = "decode_json method in Executor of RequestParser"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while decoding JSON, Please Contact with Support Team"
            logg.error('Unexpected Decoding Input Request Error' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)

        return decode_input_message

    @staticmethod
    def _json_object_hook(input_message):
        return namedtuple('X', input_message.keys())(*input_message.values())


# noinspection PyBroadException
class BasicRequestParser(object):
    def __init__(self):
        pass

    @staticmethod
    def parse(input_request):
        """
            Getting Logger Object for Executor Module
        """
        logg = PyLogs(__name__).get_pylogger()

        logg.info('Inside parsing Method')
        # print('Inside parsing Method')
        user_info = input_request.input_message.user_info
        input_message_string = input_request.input_message.input_message_bytes.decode('UTF-8')
        output_message = input_request.input_message.output_message
        socket_context = input_request.input_message.socket_context
        logger = input_request.input_message.logger

        '''
            Decoding input message string in to Python object
        '''
        logg.info('Going to decode input request')
        decoded_input_message = Decoder().decode_json(input_message_string, socket_context, logg)

        '''
            Creation Session Object for next module(Authenticator)
        '''
        logg.info('Going to create session for Authenticator')
        req_parser_session = Session(user_info, decoded_input_message, output_message, socket_context, logger)

        '''
            Prepare Authenticator Request Message and Call Authenticator
        '''
        logg.info('Calling Authenticator')
        auth_message = InputMessage(req_parser_session)
        auth_request_obj = Request(auth_message)
        auth_router_obj = Router()
        auth_router_obj.execute(auth_request_obj)