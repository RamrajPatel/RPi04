# import sys
import json
from globals import GlobalData
from collections import namedtuple


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2py(param_file_json_data):
    return json.loads(param_file_json_data)


def load_params_file(ref_LoadParamsFile, *args):
    """
        This function will return of Reference of Loaded Parameter file
        Mentioned in GlobalData
    """
    print('Inside load_params_file Method')
    param_file_json_data = open(args[0]).read()
    param_file_py_data = json2py(param_file_json_data)

    """
        Assigning the file_id as key & file records as data in 
        Global Dictionary in GlobalData.
            
        If file is Already loaded then No need to do anything, Skip Processing
    """
    if param_file_py_data["file_id"] not in GlobalData.PARAMS_FILE_OBJ_HOLDER.keys():
        GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data["file_id"]] = param_file_py_data
        print('Parameters loaded for file_id: {}'.format(param_file_py_data["file_id"]))
    else:
        print('Parameter Already Loaded for file_id: {}, Returning loaded Parameters'.format(
            param_file_py_data["file_id"]))

    """
        Calling the Constructor of Params Load Class for 
        Creating Object of this class by Passing file_id as Argument.
            
        If It's object have been created already then Object reference
        will be picked from Global Dictionary and file_id will be appended in it.
    """
    if ref_LoadParamsFile not in GlobalData.PARAMS_FILE_OBJ_HOLDER.keys():
        GlobalData.PARAMS_FILE_OBJ_HOLDER[ref_LoadParamsFile] = ref_LoadParamsFile(
            GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data["file_id"]])
    else:
        GlobalData.PARAMS_FILE_OBJ_HOLDER[ref_LoadParamsFile].load_param_list.append(
            GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data["file_id"]])
        print('Load Param File has an Object Already Created, Skipping Constructor call')

    return GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data["file_id"]]


def singelton(ref_LoadParamsFile):
    def onCall(*args):
        return load_params_file(ref_LoadParamsFile, *args)

    return onCall


@singelton
class LoadParamsFile(object):
    """
        Class will load the Parameter files for Application
        Also below list will have file_id of all the loaded Parameter files
    """
    load_param_list = []

    def __init__(self, param_file_id):
        print('Inside LoadParamsFile Constructor')
        self.load_param_list.append(param_file_id)
        print('list content is :{}'.format(self.load_param_list))