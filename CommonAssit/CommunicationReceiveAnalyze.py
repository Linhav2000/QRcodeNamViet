import enum

class CommunicationReceiveInfo:
    x = 0
    y = 0
    z = 0
    u = 0
    signal = ""
    model = ""
    algorithmName = ""
    header = ""
    action = ""
    machineType = ""
    step = 0
    axisSystemName = ""
    station = 0

class DDK_parameter:
    header = "["
    station = 1
    step = 1
    client_capture_result = 0 # 0-not yet,1-Pass/2-Fail
    client_process_result = 0 # 1-Pass/0-Fail
    client_step_tact_time = 0
    client_image_error_code = 0
    client_sw_error_code = 0
    host_request_reset = 0 # 0-None/1-Request
    client_request_reset = 0 # 0-None/1-Request
    host_motion_ready_flag = 0 # 0-Not Yet/1-Already
    client_vision_ready_flag = 1 #0-Not Yet/1-Already
    host_auto_request = 0 # 0-Auto/1-Manual
    client_auto_request = 0 # 0-Auto/1-Manual
    client_step_finish = 0 # 0-None/1-Finish
    host_auto_flag = 0 # 0-Auto/1-Manual
    client_manual_go = 0 # 0-Auto/1-Manual
    host_read_flag = 0 # 0-Ready/1-Write
    real_time = 0 # to save image name
    footer = "]"

class Info_Signal(enum.Enum):
    header = "h="
    machineType = "machine_type="
    algorithmName = "algorithm_name="
    model = "model="
    step = "step="
    axisSystemName = "as_name="
    x = "x="
    y = "y="
    z = "z="
    u = "u="

class CommandType(enum.Enum):
    roto_weighing_advance = "roto_weighing_advance"
    roto_weighing = "roto_weighing_machine"
    change_model = "change_model"
    execute_model = "execute_model"
    execute_algorithm = "execute_algorithm"
    cali_as = "cali_axis_system"
    start = "Start,CR"

def get_info_running_form(communicationReceive, mm_moving_scale=1):
    plcInfo = CommunicationReceiveInfo()
    plcReceive = communicationReceive.replace("\x00", "")
    text = ""
    try:
        dataList = str(plcReceive).split(",")
        for data in dataList:
            if data.__contains__(Info_Signal.header.value):
                try:
                    plcInfo.header = data[len(Info_Signal.header.value):]
                except Exception as error:
                    text = "ERROR Protocol: check the Header. Detail: {}".format(error)
                    return  False, plcInfo, text
            elif data.__contains__(Info_Signal.machineType.value):
                try:
                    plcInfo.machineType = data[len(Info_Signal.machineType.value):]
                except Exception as error:
                    text = "ERROR Protocol: check the machine Type. Detail: {}".format(error)
                    return  False, plcInfo, text
            elif data.__contains__(Info_Signal.model.value):
                try:
                    plcInfo.model = data[len(Info_Signal.model.value):]
                except Exception as error:
                    text = "ERROR Protocol: check the model name. Detail: {}".format(error)
                    return  False, plcInfo, text
            elif data.__contains__(Info_Signal.step.value):
                try:
                    plcInfo.step = int(data[len(Info_Signal.step.value):])
                except Exception as error:
                    text = "ERROR Protocol: step value not integer or contains white space. Detail: {}".format(error)
                    return  False, plcInfo, text
            elif data.__contains__(Info_Signal.x.value):
                try:
                    plcInfo.x = float(data[len(Info_Signal.x.value):]) / mm_moving_scale
                except Exception as error:
                    text = "ERROR Protocol: X value not float or contains white space. Detail: {}".format(error)
                    return  False, plcInfo, text
            elif data.__contains__(Info_Signal.y.value):
                try:
                    plcInfo.y = float(data[len(Info_Signal.y.value):]) / mm_moving_scale
                except Exception as error:
                    text = "ERROR Protocol: Y value not float or contains white space. Detail: {}".format(error)
                    return  False, plcInfo, text
            elif data.__contains__(Info_Signal.z.value):
                try:
                    plcInfo.z = float(data[len(Info_Signal.z.value):]) / mm_moving_scale
                except Exception as error:
                    text = "ERROR Protocol: Z value not float or contains white space. Detail: {}".format(error)
                    return  False, plcInfo, text
            elif data.__contains__(Info_Signal.u.value):
                try:
                    plcInfo.u = float(data[len(Info_Signal.u.value):]) / mm_moving_scale
                except Exception as error:
                    text = "ERROR Protocol: U value not float or contains white space. Detail: {}".format(error)
                    return  False, plcInfo, text
            elif data.__contains__(Info_Signal.axisSystemName.value):
                try:
                    plcInfo.axisSystemName = data[len(Info_Signal.axisSystemName.value):]
                except Exception as error:
                    text = "ERROR Protocol: asid is not int value or contains white space. Detail: {}".format(error)
                    return  False, plcInfo, text
        return True, plcInfo, text
    except Exception as error:
        text = "ERROR Protocol: Check the protocol. Some features cannot be convert. Detail: {}".format(error)
        return False, plcInfo, text


def getInfo_RunningForm(plcReceive, mm_moving_scale=1):
    plcInfo = CommunicationReceiveInfo()
    plcReceive = plcReceive.replace("\x00", "")
    try:
        dataList = str(plcReceive).split(",")
        cmdType = dataList[0]
        if cmdType == CommandType.roto_weighing.value:
            return getRotoWeighingInfo(plcReceive=plcReceive, mm_moving_scale=mm_moving_scale)

        text = "Command Type is wrong"
        return False, plcInfo, text
    except Exception as error:
        text = "ERROR Get plc information: {}".format(error)
        return False, plcInfo, text


def getRotoWeighingInfo(plcReceive, mm_moving_scale=1):
    text = ""
    plcInfo = CommunicationReceiveInfo()
    try:
        dataList = str(plcReceive).split(",")

        length = len(dataList)
        if length > 0:
            plcInfo.header = dataList[0]
        if length > 1:
            plcInfo.algorithmName = dataList[1]
        if length > 2:
            plcInfo.action = dataList[2]
        if length > 3:
            plcInfo.x = float(dataList[3]) / mm_moving_scale
        if length > 4:
            plcInfo.y = float(dataList[4]) / mm_moving_scale
        if length > 5:
            plcInfo.z = float(dataList[5]) / mm_moving_scale
        if length > 6:
            plcInfo.u = float(dataList[6]) / mm_moving_scale

        return True, plcInfo, text
    except Exception as error:
        text = "ERROR Get plc information: {}".format(error)
        return False, plcInfo, text

def getInfo_SignalBegin(plcReceive, mm_moving_scale=1):
    plcReceive = plcReceive.replace("\x00", "")
    try:
        plcInfo = CommunicationReceiveInfo()
        dataList = str(plcReceive).split(",")

        length = len(dataList)
        if length > 1:
            plcInfo.x = float(dataList[1]) / mm_moving_scale
        if length > 2:
            plcInfo.y = float(dataList[2]) / mm_moving_scale
        if length > 3:
            plcInfo.z = float(dataList[3]) / mm_moving_scale
        if length > 4:
            plcInfo.u = float(dataList[4]) / mm_moving_scale

        plcInfo.signal = dataList[0]

        return plcInfo
    except Exception as error:
        print("ERROR Get plc information: {}".format(error))
        return None

def getInfo_SignalEnd(plcReceive, mm_moving_scale=1):
    plcReceive = plcReceive.replace("\x00", "")
    try:

        plcInfo = CommunicationReceiveInfo()
        dataList = str(plcReceive).split(",")
        length = len(dataList)
        if length > 1:
            plcInfo.x = float(dataList[0]) / mm_moving_scale
        if length > 2:
            plcInfo.y = float(dataList[1]) / mm_moving_scale
        if length > 3:
            plcInfo.z = float(dataList[2]) / mm_moving_scale
        if length > 4:
            plcInfo.u = float(dataList[3]) / mm_moving_scale
        plcInfo.signal = dataList[length - 1]
        return plcInfo

    except Exception as error:
        print("ERROR Get plc information: {}".format(error))
        return None

def getRuConnectorInfo(plcReceive):
    plcReceive = plcReceive.replace("\x00", "")
    try:

        plcInfo = CommunicationReceiveInfo()
        dataList = str(plcReceive).split(",")
        plcInfo.y = int(dataList[0])
        plcInfo.x = int(dataList[1])
        plcInfo.z = int(dataList[2])
        return plcInfo

    except Exception as error:
        print("ERROR Get plc information: {}".format(error))
        return None

def getFuAssyInfo(plcReceive):
    plcReceive = plcReceive.replace("\x00", "")
    try:
        plcInfo = CommunicationReceiveInfo()
        dataList = str(plcReceive).split(",")
        plcInfo.y = int(dataList[0])
        plcInfo.x = int(dataList[1])
        plcInfo.z = int(dataList[2])
        plcInfo.u = int(dataList[3])
        return plcInfo
    except Exception as error:
        print("ERROR Get plc information: {}".format(error))
        return None
import copy
def getDDKInfo(plcReceive, ddk_parameter: DDK_parameter):
    temp_parm = copy.copy(ddk_parameter)
    plcReceive = plcReceive.replace("\x00", "")
    try:
        plcReceive = plcReceive[plcReceive.index("[") + 1: plcReceive.index("]")]
        dataList = str(plcReceive).split(";")
        temp_parm.station = int(dataList[0])
        temp_parm.step = int(dataList[1])
        temp_parm.host_request_reset = int(dataList[7])
        temp_parm.host_motion_ready_flag = int(dataList[9])
        temp_parm.host_auto_request = int(dataList[11])
        temp_parm.host_auto_flag = int(dataList[14])
        temp_parm.host_read_flag = int(dataList[16])
        temp_parm.real_time = dataList[17]
        return True, temp_parm
    except Exception as error:
        text = "ERROR Get plc information: {}".format(error)
        print(text)
        return False, temp_parm