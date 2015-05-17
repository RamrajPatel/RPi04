class GlobalData(object):
    """
        Class will hold global variable for Application
    """
    store_socket = {}
    PARAMS_FILE_OBJ_HOLDER = {}

    HOST_IP = '127.0.0.1'
    REQUEST_PORT = 8803
    MAX_INPUT_REQUEST_SIZE = 10240
    MAX_LISTENING_CAPACITY = 10

    """
        Queue implementation related global variables declaration starts
    """
    PARAMS_QUEUE_NAME_REF = {}
    REQ_PARSER_MAX_Q_SIZE = 50
    REQ_AUTHENTICATOR_MAX_Q_SIZE = 20
    REQ_ROUTER_MAX_Q_SIZE = 20
    SERVIC_MAX_Q_SIZE = 30
    SERVIC_CDS_MAX_Q_SIZE = 15
    MICROCONTROLLER_MAX_Q_SIZE = 20
    RES_PARSER_MAX_Q_SIZE = 10
    RES_DISPATCHER_MAX_Q_SIZE = 25

    REQ_PARSER_Q_OBJ_KEY = 'RPiReqParserQueueObjRef'
    REQ_AUTHENTICATOR_Q_OBJ_KEY = 'RPiReqAuthenticatorQueueObjRef'
    REQ_ROUTER_Q_OBJ_KEY = 'RPiReqRouterQueueObjRef'
    SERVIC_MAX_Q_OBJ_KEY = 'RPiReqServiceModuleQueueObjRef'
    SERVIC_CDS_Q_OBJ_KEY = 'RPiReqServiceCdsQueueObjRef'
    MICROCONTROLLER_Q_OBJ_KEY = 'RPiReqMicrocontrollerQueueObjRef'
    RES_PARSER_Q_OBJ_KEY = 'RPiResParserQueueObjRef'
    RES_DISPATCHER_Q_OBJ_KEY = 'RPiResDispatcherQueueObjRef'
    """
        Queue related declaration finished
    """

    DEVICE_PARAMS_FNAME = 'H:\RPi_Params\DeviceParams.json'
    DEVICE_STATES_FNAME = 'H:\RPi_Params\DevicePossibleStates.json'
    DEVICE_TYPE_ID2STATES_FNAME = 'H:\RPi_Params\DeviceTypeId2DevState.json'
    MICROCONTROLLER_PARAMS_FNAME = 'H:\RPi_Params\MicrocontrollerParams.json'
    MICROCONTROLLER_SIGNALS_FNAME = 'H:\RPi_Params\MicrocontrollerSignals.json'
    GET_ALL_DEVICE_LIST_FNAME = 'H:\RPi_Params\GetAllDevicesList.json'
    ERROR_PARAMS_FNAME = 'H:\RPi_Params\ErrorParams.json'
    SERVIE_GET_ALL_DEVICES = 'GetAllDevice'
    SERVICE_CHANGE_DEVICE_STATE = 'ChangeDeviceState'

    def __init__(self):
        pass