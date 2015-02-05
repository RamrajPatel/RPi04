__author__ = 'Ramraj'

class Session(object):
    user_info = None
    input_message = None
    output_message = None
    socket_context = None
    logger = None

    def __init__(self, user_info, input_message, output_message, socket_context, logger):
        self.user_info = user_info
        self.input_message = input_message
        self.output_message = output_message
        self.socket_context = socket_context
        self.logger = logger