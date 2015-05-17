from utilitymodule.pylogs import PyLogs
from utilitymodule.session import Session
from requestrouter.communicator import Router
from requestrouter.communicator import Request
from requestrouter.communicator import InputMessage
from authenticator.errorhandler import AuthenticatorException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.error('Inside process failure method, exiting further procesing')
    authenticator_exception_obj = AuthenticatorException(error_source, error_type, error_msg, socket_context)
    authenticator_exception_obj.process_exception()
    '''
        Exception Not yet Implemented here, Left for Future :P :D :)
    '''


class BasicAuthenticator:
    """
        This Class will authenticates Input Request and Prepare
        Request Router Triggering MetaData
    """

    def __init__(self):
        print('In Basic Authenticator')

    def authenticate(self, auth_req_obj):
        print('Inside Authenticate function of BasicAuthenticator')
        self.validate_credentials()
        self.prepare_msg(auth_req_obj)

    @staticmethod
    def validate_credentials():
        print('Inside Validate Credentials function')

    @staticmethod
    def prepare_msg(auth_req_obj):
        logg = PyLogs(__name__).get_pylogger()
        logg.info('Inside prepare message method')

        user_info = auth_req_obj.input_message.user_info
        input_message_data = auth_req_obj.input_message.input_message_data
        output_message = auth_req_obj.input_message.output_message
        socket_context = auth_req_obj.input_message.socket_context
        logger = auth_req_obj.input_message.logger

        '''
            Creation Session Object for next module(Request Router)
        '''
        logg.info('Creating Session object for Router Module')
        req_router_session = Session(user_info, input_message_data, output_message, socket_context, logger)

        '''
            Prepare Router request and Call Service Router Module
        '''
        logg.info('Calling Router Module')
        auth_message = InputMessage(req_router_session)
        req_router_request_obj = Request(auth_message)
        req_router_router_obj = Router()
        req_router_router_obj.execute(req_router_request_obj)