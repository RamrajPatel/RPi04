import sys
import socket
from utilitymodule.pylogs import PyLogs


class BasicTcpResponseDispatcher(object):
    def __init__(self):
        pass

    @staticmethod
    def send_reply(req_tcp_res_disp_obj):
        # print('in Send_Reply in BasicTcpResponseDispatcher ')
        logg = PyLogs(__name__).get_pylogger()
        logg.info('in Send_Reply in BasicTcpResponseDispatcher ')
        try:
            socket_context = req_tcp_res_disp_obj.output_response.socket_context
        except (AttributeError, TypeError) as err_message:
            logg.error('Error while fetching socket context')
            print('Res Dispatcher: Executor: BasicTcpResponseDispatcher: send_reply: check 1')
            print('Connection Error, Error Code {} and Error Message: {}'.format(err_message[0], err_message[1]))
            sys.exit()

        try:
            socket_context.sendall(req_tcp_res_disp_obj.output_response.output_message)
        except socket.error as err_message:
            logg.error('Error while sending data to client')
            print('Res Dispatcher: Executor: BasicTcpResponseDispatcher: send_reply: check 2')
            print('Data to client failed, Error Code {} and Error Message: {}'.format(err_message[0], err_message[1]))
            sys.exit()

        print('Response Sent to Client is Successful')
        logg.info('Response Sent to Client is Successful')

        try:
            socket_context.close()
        except socket.error as err_message:
            logg.error('Socket close error')
            print('Res Dispatcher: Executor: BasicTcpResponseDispatcher: send_reply: check 3')
            print('Socket Closing Error, Error Code {} and Error Message: {}'.format(err_message[0], err_message[1]))
            sys.exit()
        # print('Response Dispatcher Connection Close')