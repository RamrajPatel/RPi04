import sys
from utilitymodule.pylogs import PyLogs
from utilitymodule import loadparamfile
from microcontroller.errorhandler import MicroControllerException


def process_failure(error_source, error_type, error_msg, socket_context, logg):
    logg.info('Inside process failure, exiting further processing')
    mc_exception_obj = MicroControllerException(error_source, error_type, error_msg, socket_context)
    mc_exception_obj.process_exception()


class MicroParameters(object):
    """
        This Class will Return all Parameter values requested for MicroController
        Module
    """

    def __init__(self):
        pass

    @staticmethod
    def get_device_params_file_name():
        return loadparamfile.GlobalData.DEVICE_PARAMS_FNAME

    @staticmethod
    def get_device_states_file_name():
        return loadparamfile.GlobalData.DEVICE_STATES_FNAME

    @staticmethod
    def get_device_type_id2states_file_name():
        return loadparamfile.GlobalData.DEVICE_TYPE_ID2STATES_FNAME

    @staticmethod
    def get_microcontroller_params_file_name():
        return loadparamfile.GlobalData.MICROCONTROLLER_PARAMS_FNAME

    @staticmethod
    def get_microcontroller_signals_file_name():
        return loadparamfile.GlobalData.MICROCONTROLLER_SIGNALS_FNAME

    @staticmethod
    def get_device_type_id(device_id, ref_device_param):
        print('Inside get_device_type_id Method')
        if device_id in ref_device_param["file_data"]:
            if 'device_type_id' in ref_device_param["file_data"][device_id]:
                return ref_device_param["file_data"][device_id]["device_type_id"]
            else:
                print('Device Not Mapped to any device_type_id, Check Device Params')
                return False
        else:
            print('Device Not Found in Device Params, Error')
            return False

    @staticmethod
    def get_micontroller_id(device_id, ref_device_param):
        print('inside get_micontroller_id Method')
        if device_id in ref_device_param["file_data"]:
            if 'module_id' in ref_device_param["file_data"][device_id]:
                return ref_device_param["file_data"][device_id]["module_id"]
            else:
                print('Device is not mapped to any MicroController, check Device Params, Error')
                return False
        else:
            print('Device Not found in Device Params, Error')
            return False

    @staticmethod
    def get_device_type_state_id(device_type_id, ref_device_type_id2states):
        print('Inside get_device_type_state_id Method')
        if device_type_id in ref_device_type_id2states["file_data"]:
            if 'states_id' in ref_device_type_id2states["file_data"][device_type_id]:
                return ref_device_type_id2states["file_data"][device_type_id]["states_id"]
            else:
                print('No State Id Attached with Device Type Id, Check DeviceTypeID2States Params, Error')
                return False
        else:
            print('Device Type State Id Not found in Param Files, Error')
            return False

    @staticmethod
    def get_device_signal_id(device_id, ref_device_param):
        print('Inside get_device_signal_id Method')
        if device_id in ref_device_param["file_data"]:
            if 'signal_id' in ref_device_param["file_data"][device_id]:
                return ref_device_param["file_data"][device_id]["signal_id"]
            else:
                print('No Signal ID Attached with Device, Check Device params, Error')
                return False
        else:
            print('Device Signal Not Found in Params file, Error')
            return False

    """
    def get_devcie_state_signal_id(self, device_type_state_id, desired_device_state, ref_device_state):
        return ref_device_state["file_data"][device_type_state_id][desired_device_state]["signal_id"]
    """

    @staticmethod
    def get_devcie_state_signal_id(device_type_state_id, desired_device_state, ref_device_state):
        """
            Implemented Fall Back Concept
        """
        print('Inside get_devcie_state_signal_id Method')
        if device_type_state_id in ref_device_state["file_data"]:
            if desired_device_state in ref_device_state["file_data"][device_type_state_id]:
                return ref_device_state["file_data"][device_type_state_id][desired_device_state]["signal_id"]
            else:
                print('Mapping signal not found fetching if Default tag is Present')
                if 'default_tag' in ref_device_state["file_data"][device_type_state_id]:
                    default_tag_val = ref_device_state["file_data"][device_type_state_id]['default_tag']
                    return ref_device_state["file_data"][default_tag_val][desired_device_state]["signal_id"]
                else:
                    print('No default mapping found for this tag error')
                    return False
        else:
            print('No state ID Mapping found in Parameter file')
            return False

    @staticmethod
    def get_microcontroller_signal_id(module_id, ref_mc_param):
        if module_id in ref_mc_param["file_data"]:
            if 'signal_id' in ref_mc_param["file_data"][module_id]:
                return ref_mc_param["file_data"][module_id]["signal_id"]
            else:
                print('MicroController Signal Not Found, Check MC Params, Error')
                return False
        else:
            print('MicroController ID Not found in MicroController Params, Error')
            return False

    """
    def get_hex_device_id_signal(self, device_signal_id, ref_mc_signal):
        return ref_mc_signal["file_data"][device_signal_id]["signal"]
    """

    @staticmethod
    def get_hex_device_id_signal(device_signal_id, ref_mc_signal):
        """
            Implemented Fall Back Concept
        """
        if device_signal_id in ref_mc_signal["file_data"]:
            if 'signal' in ref_mc_signal["file_data"][device_signal_id]:
                return ref_mc_signal["file_data"][device_signal_id]["signal"]
            else:
                print('Signal Mapping Not Found, Fetching from Default if any')
                if 'default_tag' in ref_mc_signal["file_data"][device_signal_id]:
                    default_tag_val = ref_mc_signal["file_data"][device_signal_id]['default_tag']
                    if device_signal_id in ref_mc_signal["file_data"][default_tag_val]:
                        return ref_mc_signal["file_data"][default_tag_val][device_signal_id]
                    else:
                        print('No Signal in File Default Tag, Error')
                        return False
                else:
                    print('No Default Mapping too found for this signal, Skipping Processing, Error')
                    return False
        else:
            print("No Signal found for this Signal Id, Throwing Error")
            return False

    """    
    def get_hex_device_state_signal(self, device_state_signal_id, ref_mc_signal):
        return ref_mc_signal["file_data"][device_state_signal_id]["signal"]
    """

    @staticmethod
    def get_hex_device_state_signal(device_state_signal_id, ref_mc_signal):
        """
            Implemented Fall Back Concept For Device State MicroController Signal
        """
        print('Inside Device State Signal Method')
        if device_state_signal_id in ref_mc_signal["file_data"]:
            if 'signal' in ref_mc_signal["file_data"][device_state_signal_id]:
                return ref_mc_signal["file_data"][device_state_signal_id]["signal"]
            else:
                print('Signal Mapping Not Found, Fetching from Default if any')
                if 'default_tag' in ref_mc_signal["file_data"][device_state_signal_id]:
                    default_tag_val = ref_mc_signal["file_data"][device_state_signal_id]['default_tag']
                    if device_state_signal_id in ref_mc_signal["file_data"][default_tag_val]:
                        return ref_mc_signal["file_data"][default_tag_val][device_state_signal_id]
                    else:
                        print('No Signal in File Default Tag, Error')
                        return False
                else:
                    print('No Default Mapping too found for this signal, Skipping Processing, Error')
                    return False
        else:
            print("No Signal found for this Signal Id, Throwing Error")
            return False

    """
    def get_hex_microcontroller_signal(self, module_signal_id, ref_mc_signal):
        return ref_mc_signal["file_data"][module_signal_id]["signal"]
    """

    @staticmethod
    def get_hex_microcontroller_signal(module_signal_id, ref_mc_signal):
        """
            Implemented Fall-Back Concept for MicroController Signal
        """
        print('Inside MicroController Signal Method')
        if module_signal_id in ref_mc_signal["file_data"]:
            if 'signal' in ref_mc_signal["file_data"][module_signal_id]:
                return ref_mc_signal["file_data"][module_signal_id]["signal"]
            else:
                print('Signal Mapping Not Found, Fetching from Default if any')
                if 'default_tag' in ref_mc_signal["file_data"][module_signal_id]:
                    default_tag_val = ref_mc_signal["file_data"][module_signal_id]['default_tag']
                    if module_signal_id in ref_mc_signal["file_data"][default_tag_val]:
                        return ref_mc_signal["file_data"][default_tag_val][module_signal_id]
                    else:
                        print('No Signal in File Default Tag, Error')
                        return False
                else:
                    print('No Default Mapping too found for this signal, Skipping Processing, Error')
                    return False
        else:
            print("No Signal found for this Signal Id, Throwing Error")
            return False


class Microcontroller(object):
    """
        Main GPIO Class for MicroController Device
        This Class will sent a request to MicroController for actual Processing
        This Class will Act like a Client Program for MicroController
    """
    device_signal = None
    device_state_signal = None
    module_signal = None

    def __init__(self, device_signal, device_state_signal, module_signal):
        self.device_signal = device_signal
        self.device_state_signal = device_state_signal
        self.module_signal = module_signal

    @staticmethod
    def send_data():
        print('Data sent to microController Programs')


class MicrocontrollerInterface(object):
    """
        This is the Core Important class of whole Module.
        Here Only Specific task will be performed according
        to given Request Message and Response Will be Routed
        to Response Parser Module
    """

    def __init__(self):
        pass

    @staticmethod
    def process(mc_request, mc_response):
        # print('Inside process Method of Micro-controller Interface Class')
        logg = PyLogs(__name__).get_pylogger()
        logg.info('Inside process Method of Micro-controller Interface Class')
        socket_context = mc_request.socket_context

        mc_param_obj = MicroParameters()
        ref_device_param = None
        ref_device_state = None
        ref_device_type_id2states = None
        ref_mc_param = None
        ref_mc_signal = None
        device_signal = None
        device_state_signal = None
        module_signal = None
        # noinspection PyBroadException
        try:
            """
                Loading Device Parameters
            """
            logg.info('Loading Device Params')
            device_param_file = mc_param_obj.get_device_params_file_name()
            ref_device_param = loadparamfile.LoadParamsFile(device_param_file)
            print(ref_device_param)

            """
                Loading Device Type States Parameters
            """
            logg.info('Loading Device Type States Parameters')
            device_state_file = mc_param_obj.get_device_states_file_name()
            ref_device_state = loadparamfile.LoadParamsFile(device_state_file)
            print(ref_device_state)

            """
                Loading Device Type Parameters
            """
            logg.info('Loading Device Type Parameters')
            device_type_id2states_file = mc_param_obj.get_device_type_id2states_file_name()
            ref_device_type_id2states = loadparamfile.LoadParamsFile(device_type_id2states_file)
            print(ref_device_type_id2states)

            """
                Loading MicroController Parameters
            """
            logg.info('Loading MicroController Parameters')
            mc_param_file = mc_param_obj.get_microcontroller_params_file_name()
            ref_mc_param = loadparamfile.LoadParamsFile(mc_param_file)
            print(ref_mc_param)

            """
                Loading MicroController Hardware Signals Parameters
            """
            logg.info('Loading MicroController Hardware Signals Parameters')
            mc_signal_file = mc_param_obj.get_microcontroller_signals_file_name()
            ref_mc_signal = loadparamfile.LoadParamsFile(mc_signal_file)
            print(ref_mc_signal)
        except ValueError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            error_msg = "ValueError, params file load error"
            logg.error('Param files load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except TypeError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            error_msg = "TypeError, param file load error"
            logg.error('Param files load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except EOFError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            error_msg = "EOFError, params file is empty"
            logg.error('Param files load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except IOError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            error_msg = "IOError, loding param file error"
            logg.error('Param files load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except AttributeError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            error_msg = "AttributeError while Fetching param files"
            logg.error('Param files load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except:
            error_source = "process method in Executor of MicroController"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Fetching params files"
            logg.error('Param files load error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)

        # noinspection PyBroadException
        try:
            """
                Fetching Device Type Id, Module Id(MicroController Id) and Device
                Signal Id for Further Processing
            """
            device_type_id = mc_param_obj.get_device_type_id(mc_request.device_id, ref_device_param)
            module_id = mc_param_obj.get_micontroller_id(mc_request.device_id, ref_device_param)
            print('data is: {} : {} '.format(device_type_id, module_id))

            """
                Now Fetching Device Type States IDs and Signal IDs for Device,
                Device States and MicrController
            """
            device_signal_id = mc_param_obj.get_device_signal_id(mc_request.device_id, ref_device_param)
            device_type_state_id = mc_param_obj.get_device_type_state_id(device_type_id, ref_device_type_id2states)
            device_state_signal_id = mc_param_obj.get_devcie_state_signal_id(device_type_state_id,
                                                                             mc_request.desired_device_state,
                                                                             ref_device_state)
            module_signal_id = mc_param_obj.get_microcontroller_signal_id(module_id, ref_mc_param)

            """
                Finally Fetching Hardware Triggering MicrController Signal for device,
                Device state and MicroController
            """
            device_signal = mc_param_obj.get_hex_device_id_signal(device_signal_id, ref_mc_signal)
            device_state_signal = mc_param_obj.get_hex_device_state_signal(device_state_signal_id, ref_mc_signal)
            module_signal = mc_param_obj.get_hex_microcontroller_signal(module_signal_id, ref_mc_signal)
        except ValueError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            error_msg = "ValueError, params file load error"
            logg.error('Param files fetch value error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except TypeError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            logg.error('Param files fetch value error, Reason: ' + error_type)
            error_msg = "TypeError, param file load error"
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except KeyError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            error_msg = "KeyError, param file load error"
            logg.error('Param files fetch value error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except IndexError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            error_msg = "IndexError, param file load error"
            logg.error('Param files fetch value error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except EOFError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            error_msg = "EOFError, params file is empty"
            logg.error('Param files fetch value error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except IOError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            error_msg = "IOError, loding param file error"
            logg.error('Param files fetch value error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except AttributeError as mc_error_msg:
            error_source = "process method in Executor of MicroController"
            error_type = mc_error_msg.__class__.__name__
            error_msg = "AttributeError while Fetching param files"
            logg.error('Param files fetch value error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)
        except:
            error_source = "process method in Executor of MicroController"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Fetching params files"
            logg.error('Param files fetch value error, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)

        """
            Passing These Control Signals To MicroController Module for Hardware
            Processing(Calling Send data Function to Send signal to MicroController)
            Write Response of MicroController in Response Class for Further Decision
            Making
        """
        # noinspection PyBroadException
        try:
            logg.info('Passing Control Signals to Micro-controller')
            mc_obj = Microcontroller(device_signal, device_state_signal, module_signal)
            mc_obj.send_data()
        except:
            error_source = "process method in Executor of MicroController"
            error_type = sys.exc_info()[0].__name__
            error_msg = "Unexpected Error while Hardware Processing"
            logg.error('Error while Hradware Processing, Reason: ' + error_type)
            process_failure(error_source, error_type, error_msg, socket_context, logg)

        """
            For Time being HardCoded Positive Acknowledgement have been
            sent back.
            At time of actual Processing, please change Accordingly
        """
        logg.info('Returning Positivve Response from Mixro-Controller Module to Service')
        mc_response.response_message = "OK"
        return mc_response