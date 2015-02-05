"""
    socket_context and connection_details are same
"""

import sys
import socket
# import uuid  # For Generating Random String for Incoming Request
from globals import GlobalData
from requestparser.communicator import Router
from requestparser.communicator import Request
from requestparser.communicator import InputMessage
from concurrent.futures.thread import ThreadPoolExecutor
from utilitymodule.pylogs import PyLogs
from tcprequestdispatcher.errorhandler import ReqDispatcherException


def process_failure(error_source, error_type, error_msg, connection_details):
    req_disp_exception_obj = ReqDispatcherException(error_source, error_type, error_msg, connection_details)
    req_disp_exception_obj.process_exception()


class Session(object):
    user_info = None
    input_message = None
    output_message = None
    socket_context = None
    logger = None

    def __init__(self, user_info, input_message, connection, logg):
        self.user_info = user_info
        self.input_message = input_message
        self.output_message = {"comm_msg": {}}
        self.socket_context = connection
        self.logger = logg


class BasicTCPRequestDispatcher(object):
    """
        Initial class from where Processing will initiate
        Client Request will be accepted here only and
        scheduled to take appropriate Action
    """

    @staticmethod
    def dispatch_connection(connection):
        print('Dispatching Received Request')
        '''
            Geting Logger Object
        '''
        my_logger = PyLogs(__name__)
        logg = my_logger.get_pylogger()
        logg.info('Logger object created')

        ''' Receiving Input Request from client '''
        # noinspection PyBroadException
        try:
            '''@TODO input request size '''
            input_request_data = connection.recv(GlobalData.MAX_INPUT_REQUEST_SIZE)
            # print('Input data from HTTP client is:', input_request_data)
            logg.info('Input data from HTTP client is:' + str(input_request_data))

            """
                Generation of transaction based session from dispatcher received data
                How will i get user info for session object ??
                Currently Hardcoding the user information for authenticate user
            """
            user_info = '{"user_id" : "RRP00001", "user_name" : "Ramraj Patel"}'
            req_dsipatcher_session = Session(user_info, input_request_data, connection, logg)
            logg.info('Session Object Created, Triggering Request Parser')

            # req_parser_comm_obj = InputMessage('TCP', input_request_data, connection)
            req_parser_comm_obj = InputMessage('TCP', req_dsipatcher_session)
            req_parser_request_obj = Request(req_parser_comm_obj)
            req_parser_router_obj = Router()
            req_parser_router_obj.execute(req_parser_request_obj)
        except socket.error as req_dispatch_error_msg:
            error_source = "Executor of TCPRequestDispatcher"
            error_type = req_dispatch_error_msg.__class__.__name__
            error_msg = "Problem in Dispatching Connection, Please Contact with Support Team"
            logg.error('Server Connection Dispatching Error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, connection)
        except:
            error_source = "Executor of TCPRequestDispatcher"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error in Dispatching Connection, Please Contact with Support Team"
            # logg.error('Socket bind fail, Reason: ' + error_type)
            logg.error('Unexpected Server Connection Dispatching Error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, connection)


if __name__ == '__main__':
    # '''
    #     Geting Logger Object
    # '''
    # my_logger = PyLogs()
    # logg = my_logger.get_pylogger()
    # # logg.flush()
    # logg.info('Logger object created')

    socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print('Socket created')
    # logg.info('Socket created')

    ''' Bind socket to local host and port  '''
    # noinspection PyBroadException
    try:
        socketObj.bind((GlobalData.HOST_IP, GlobalData.REQUEST_PORT))
        # logg.info('Socket bind complete')
        print('Socket bind complete')

    except socket.error as bind_fail_err:
        error_source = "Executor of TCPRequestDispatcher"
        error_type = bind_fail_err.__class__.__name__
        error_msg = "Server Socket Binding Fail"
        # logg.error('Socket bind fail, Reason: ' + error_type)
        # error_code=155
        # process_failure(error_source, error_type, error_msg)
        sys.exit()
    except:
        # logg.error('Socket bind fail')
        error_source = "Executor of TCPRequestDispatcher"
        error_type = sys.exc_info()[0].__name__
        error_msg = "Unexpected Error while Socket Binding"
        # logg.error('Socket bind fail, Reason: ' + error_type)
        # error_code=155
        # process_failure(error_source, error_type, error_msg)
        sys.exit()

    '''  Start listening on socket '''
    # noinspection PyBroadException
    try:
        # socketObj.listen(10)
        socketObj.listen(GlobalData.MAX_LISTENING_CAPACITY)
        print('Socket is Now listening Mode')
        # logg.info('Socket is Now listening Mode')
    except socket.error as listen_fail_err:
        error_source = "Executor of TCPRequestDispatcher"
        error_type = listen_fail_err.__class__.__name__
        error_msg = "Server Socket Listening Problem"
        # logg.error('Socket listening error, Reason: ' + error_type)
        # error_code=155
        # process_failure(error_source, error_type, error_msg)
        sys.exit()
    except:
        # logg.error('Socket listening exception')
        error_source = "Executor of TCPRequestDispatcher"
        error_type = sys.exc_info()[0].__name__
        error_msg = "Unexpected Error while Listening"
        # logg.error('Socket listening error, Reason: ' + error_type)
        # error_code=155
        # process_failure(error_source, error_type, error_msg)
        sys.exit()

    tcp_req_obj = BasicTCPRequestDispatcher()

    connection_details = None
    ''' now keep talking with the client '''
    while True:
        '''    wait to accept a connection - blocking call    '''
        # global connection_details
        # noinspection PyBroadException
        try:
            connection_details, address = socketObj.accept()
            # logg.info('Socket connected to:' + address[0] + ':' + str(address[1]))
            print('Connected with ' + address[0] + ':' + str(address[1]))
            # err_socket_context = connection_details
            # global err_socket_context

        except socket.error as conn_accept_fail_err:
            error_source = "In MAIN of Executor of TCPRequestDispatcher"
            error_type = conn_accept_fail_err.__class__.__name__
            error_msg = "Server Socket Connection Accept Problem"
            # logg.error('Socket connecting to client fail, Reason: ' + error_type)
            # error_code=155
            process_failure(error_source, error_type, error_msg, connection_details)
        except:
            # logg.error('Socket connecting to client fail')
            error_source = "In MAIN of Executor of TCPRequestDispatcher"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Accepting Connection"
            # logg.error('Socket connecting to client fail, Reason: ' + error_type)
            # error_code=155
            process_failure(error_source, error_type, error_msg, connection_details)

        '''
            start new thread takes 1st argument as a function
            name to be run, second is the tuple of arguments to
            the function.
            _thread.start_new_thread(client thread ,(conn,))
            use Thread pool to service the clients.
        '''
        try:
            with ThreadPoolExecutor(max_workers=3) as executor:
                f1 = executor.submit(tcp_req_obj.dispatch_connection(connection_details))
                # f1 = executor.submit(tcp_req_obj.dispatch_connection(connection_details, logg))
        except Exception as thread_pool_fail_msg:
            error_source = "In MAIN of Executor of TCPRequestDispatcher"
            error_type = thread_pool_fail_msg.__class__.__name__
            error_msg = "Thread Creation Aborted, Exiting Program"
            # logg.error('Aborting Thread Pool, Reason: ' + error_type)
            # error_code=155
            process_failure(error_source, error_type, error_msg, connection_details)

    # logg.info('Client processing Done, closing Server Socket')
    # noinspection PyBroadException
    try:
        socketObj.close()
        # logg.info('Server Socket Closing Done, Exiting Program')
    except socket.error as socket_close_err:
        error_source = "In MAIN of Executor of TCPRequestDispatcher"
        error_type = socket_close_err.__class__.__name__
        error_msg = "Server Socket Closing Problem, Exiting Program"
        # logg.error('Server Socket Closing Error, Reason: ' + error_type)
        # error_code=155
        process_failure(error_source, error_type, error_msg, connection_details)
    except:
        error_source = "In MAIN of Executor of TCPRequestDispatcher"
        error_type = sys.exc_info()[0].__name__
        error_msg = "Unexpected Error while Closing Connection, Exiting Program"
        # logg.error('Server Socket Closing Error, Reason: ' + error_type)
        # error_code=155
        process_failure(error_source, error_type, error_msg, connection_details)