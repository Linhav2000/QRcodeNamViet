import enum

class ReceivePLCCmd:
    signal = ""
    fullForm = ""

    def __init__(self, signal, fullForm):
        self.signal = signal
        self.fullForm = fullForm

    def getData(self, plcData):
        data = str(plcData).replace("\x00", "")
        signalPos = data.find(self.signal)
        startPos = signalPos - len(self.fullForm) + len(self.signal)
        endPos = startPos + len(self.fullForm)
        revCurrentData = plcData[startPos:endPos]
        return revCurrentData

    def getDataRuConnectorForm(self, plcData):
        data = str(plcData).replace("\x00", "")
        signalPos = plcData.find(self.signal)
        startPos = signalPos
        endPos = startPos + len(self.fullForm)
        revCurrentData = plcData[startPos:endPos]

        return revCurrentData

    def getDataFuAssy(self, plcData):
        data = str(plcData).replace("\x00", "")
        dataList = data.split("CR")
        for data in dataList:
            if data.__contains__(self.signal):
                return data
        return ""
    # def split_ddk_cmd(self, plcData):
    #     data = str(plcData).replace("\x00", "")
    #     dataList = data.split("[")
    #     for dat



class PLCCommunicationFrame(enum.Enum):
    # Connection checking
    revReady = ReceivePLCCmd("READY", "READY")

    sendReady = "READY"

    # conversion coefficient
    sendStartConvert = "00000,00000,00000,CONVE1"  # 00000,00000,00000,CONVE1
    sendConvert2Pos = "{},{},{},CONVE2"  # XXXXX,YYYYY,ZZZZZ,CONVE2
    sendDoneConvert2 = "CONVERT3"  #

    # revConvert1 = "CONVE1"                          # XXXXX,YYYYY,ZZZZZ,CONVE1
    # revConvert2 = "CONVE2"                          # XXXXX,YYYYY,ZZZZZ,CONVE2

    revConvert1 = ReceivePLCCmd("CONVE1", "XXXXX,YYYYY,ZZZZZ,CONVE1")
    revConvert2 = ReceivePLCCmd("CONVE2", "XXXXX,YYYYY,ZZZZZ,CONVE2")
    # revConvertLength = 24

    # Cali Offset
    sendStartCaliOffset = "00000,00000,00000,OFFSETS"  # 00000,00000,00000,OFFSETS
    sendChangeCaliPos = "{},{},{},OFFSETC"  # XXXXX,YYYYY,ZZZZZ,OFFSETC
    sendOffset1 = "00000,00000,00000,OFFSET1"  # 00000,00000,00000,OFFSET1

    # revStartCaliOffset = "OFFSETS"                  # XXXXX,YYYYY,ZZZZZ,OFFSETS
    # revOffsetChangeDone = "OFFSETC"                 # XXXXX,YYYYY,ZZZZZ,OFFSETC
    # revOffset1 = "OFFSET1"                          # XXXXX,YYYYY,00000,OFFSET1

    revStartCaliOffset = ReceivePLCCmd("OFFSETS", "XXXXX,YYYYY,ZZZZZ,OFFSETS")
    revOffsetChangeDone = ReceivePLCCmd("OFFSETC", "XXXXX,YYYYY,ZZZZZ,OFFSETC")
    revOffset1 = ReceivePLCCmd("OFFSET1", "XXXXX,YYYYY,00000,OFFSET1")
    # revOffsetLength = 25

    # Running cmd from PLC
    # revRunning = "00000,00000,00000,RUN"            # 00000,00000,00000,RUN
    revRunning = ReceivePLCCmd("RUN", "00000,00000,00000,RUN")

    # revRunningLength = 21

    # revStart = "START"                              # 1111-1111-1111,START (barcode serial - 12 characters)
    revStart = ReceivePLCCmd("START", "1111-1111-1111,START")

    # revStartLength = 23

    # revTrigA = "TRIGA"                              # XXXXX,YYYYY,ZZZZZ,TRIGA
    # revTrigB = "TRIGB"                              # XXXXX,YYYYY,ZZZZZ,TRIGB
    # revTrigC = "TRIGC"                              # XXXXX,YYYYY,ZZZZZ,TRIGC
    # revRequestPoint = "TRIGP"                       # 00000,00000,00000,TRIGP00 -> 00000,00000,00000,TRIGPn

    revTrigA = ReceivePLCCmd("TRIGA", "XXXXX,YYYYY,ZZZZZ,TRIGA")
    revTrigB = ReceivePLCCmd("TRIGB", "XXXXX,YYYYY,ZZZZZ,TRIGB")
    revTrigC = ReceivePLCCmd("TRIGC", "XXXXX,YYYYY,ZZZZZ,TRIGC")
    revRequestPoint = ReceivePLCCmd("TRIGP", "XXXXX,YYYYY,ZZZZZ,TRIGP")

    # revTrigLength = 23

    revReceive = ReceivePLCCmd("RECEIVE", "RECEIVE")  # RECEIVE
    revDesignShow = ReceivePLCCmd("DESIGN", "DESIGN")

    # Running cmd to PLC
    sendRunning = '{},{},RUN'  # 123,AAAA-AAAA-AAAA,RUN (number of points - 3 character, model name - 12 characters, RUN)
    sendTrigA = "{},{},{},TRIGA"  # XXXXX,YYYYY,ZZZZZ,TRIGA
    sendTrigB = "{},{},{},TRIGB"  # XXXXX,YYYYY,ZZZZZ,TRIGB
    sendTrigC = "{},{},{},TRIGC"  # XXXXX,YYYYY,ZZZZZ,TRIGC
    sendDoneCalculation = '00000,00000,00000,TRIGP'  # 00000,00000,00000,TRIGP

    sendPositionForm = "{},{},{},OK"  # XXXXX,YYYYY,00000,OK (for OK point)
    sendFinishPositionForm = "{},{},{},CR"  # XXXXX,YYYYY,00000,CR (for last point)
    sendNGPositionForm = "{},{},{},NG"  # XXXXX,YYYYY,00000,NG (for NG point)

    # Current working position
    revCurrentWorkingPosition = ReceivePLCCmd("CURRENT", "012,OK,CURRENT")


class RUConnectorComFrame(enum.Enum):
    # Connection checking
    revReady = ReceivePLCCmd("READY", "READY")

    sendReady = "READY"

    # conversion coefficient
    sendStartConvert = "000000,000000,000000,CONVER1"  # 000000,000000,000000,CONVER1
    sendConvert2Pos = "{},{},{},CONVER2"  # XXXXXX,YYYYYY,ZZZZZZ,CONVER2
    sendDoneConvertDone = "000000,000000,000000,CONVERD"  # "000000,000000,000000,CONVERD"

    revConvert1 = ReceivePLCCmd("CONVER1", "XXXXXX,YYYYYY,ZZZZZZ,CONVER1")
    revConvert2 = ReceivePLCCmd("CONVER2", "XXXXXX,YYYYYY,ZZZZZZ,CONVER2")

    # Cali Offset
    sendStartCaliOffset = "XXXXXX,YYYYYY,ZZZZZZ,OFFSETS"  # XXXXXX,YYYYYY,ZZZZZZ,OFFSETS
    sendChangeCaliPos = "{},{},{},OFFSETC"  # XXXXXX,YYYYYY,ZZZZZZ,OFFSETC
    sendCaliOffsetDone = "XXXXXX,YYYYYY,ZZZZZZ,OFFSETD"  # XXXXXX,YYYYYY,ZZZZZZ,OFFSETD
    sendOffset1 = "XXXXXX,YYYYYY,ZZZZZZ,OFFSET1"  # XXXXXX,YYYYYY,ZZZZZZ,OFFSET1

    revStartCaliOffset = ReceivePLCCmd("OFFSETS", "XXXXXX,YYYYYY,ZZZZZZ,OFFSETS")
    revOffsetChangeDone = ReceivePLCCmd("OFFSETC", "XXXXXX,YYYYYY,ZZZZZZ,OFFSETC")
    revOffset1 = ReceivePLCCmd("OFFSET1", "XXXXXX,YYYYYY,ZZZZZZZ,OFFSET1")

    # Running cmd from PLC
    revRunning = ReceivePLCCmd("RUN", "XXXXXX,YYYYYY,ZZZZZZ,RUN")

    # revStart = "START"                              # 1111-1111-1111,START (barcode serial - 11 characters)
    revStart = ReceivePLCCmd("START", "11111111111,START")

    revTrigA = ReceivePLCCmd("TRIG1", "XXXXXX,YYYYYY,ZZZZZZ,TRIG1")
    revTrigB = ReceivePLCCmd("TRIG2", "XXXXXX,YYYYYY,ZZZZZZ,TRIG2")
    revTrigC = ReceivePLCCmd("TRIG3", "XXXXXX,YYYYYY,ZZZZZZ,TRIG3")
    revRequestPoint = ReceivePLCCmd("TRIGP", "XXXXXX,YYYYYY,ZZZZZZ,TRIGP")

    revReceive = ReceivePLCCmd("RECEIVE", "RECEIVE")  # RECEIVE
    revDesignShow = ReceivePLCCmd("DESIGN", "DESIGN")

    # Running cmd to PLC
    sendRunning = '{},{},ZZZZZZ,RUN'  # 123,AAAA-AAAA-AAAA,RUN (number of points - 3 character, model name - 12 characters, RUN)
    sendTrigA = "{},{},{},TRIG1"  # XXXXXX,YYYYYY,ZZZZZZ,TRIGA
    sendTrigB = "{},{},{},TRIG2"  # XXXXXX,YYYYYY,ZZZZZZ,TRIGB
    sendTrigC = "{},{},{},TRIG3"  # XXXXXX,YYYYYY,ZZZZZZ,TRIGC
    sendDoneCalculation = 'XXXXXX,YYYYYY,ZZZZZZ,TRIGD'  # XXXXXX,YYYYYY,ZZZZZZ,TRIGD

    sendPositionForm = "{},{},{},OK"  # XXXXXX,YYYYYY,ZZZZZZ,OK (for OK point)
    sendFinishPositionForm = "{},{},{},CR"  # XXXXXX,YYYYYY,ZZZZZZ,CR (for last point)
    sendNGPositionForm = "{},{},{},NG"  # XXXXXX,YYYYYY,ZZZZZZ,NG (for NG point)

    # Current working position
    revCurrentWorkingPosition = ReceivePLCCmd("CURRENT", "012,OK,CURRENT")

    revFinish = ReceivePLCCmd("FINISH", "FINISH")

    # Missing check position
    revMissingCheckPosition = ReceivePLCCmd("POSITION", "POSITION00,OK")
    sendMissingCheckOK = "XXXXXX,YYYYYY,ZZZZZZ,DONE{},OK"
    sendMissingCheckNG = "XXXXXX,YYYYYY,ZZZZZZ,DONE{},NG"
    sendMissingCheckCR = "XXXXXX,YYYYYY,ZZZZZZ,DONE{},CR"

class RearCheckMissingComFrame(enum.Enum):
    revTakePicLeft = ReceivePLCCmd("LEFT", "LEFT")
    revTakePicRight = ReceivePLCCmd("RIGHT", "RIGHT")

    sendRightOk = "R_OK"
    sendRightNG = "R_NG"
    sendLeftOk = "L_OK"
    sendLeftNG = "L_NG"

class LocationDemoComFrame(enum.Enum):
    revTakePic = ReceivePLCCmd("TAKEPIC", "TAKEPIC")
    revResultDone = ReceivePLCCmd("R-Result", "R-Result")

    sendGetTakePicSignal = "R-TAKEPIC"
    sendOK = "OK"
    sendNG = "NG"

class FU_Assy_ComFrame(enum.Enum):
    # convert pixel to mm
    sendStartConvertRU = "00000,00000,00000,00000,CONVERTA,1,"
    sendConvertRU2Pos = "{},{},{},{},CONVERTA,2,"
    sendConvertRUDone = "00000,00000,00000,00000,CONVERTA,D,"

    sendStartConvertFU = "00000,00000,00000,00000,CONVERTB,1,"
    sendConvertFU2Pos = "{},{},{},{},CONVERTB,2,"
    sendConvertFUDone = "00000,00000,00000,00000,CONVERTB,D,"

    revConvertRU1 = ReceivePLCCmd("CONVERTA,1", "00000,00000,00000,00000,CONVERTA,1")
    revConvertRU2 = ReceivePLCCmd("CONVERTA,2", "00000,00000,00000,00000,CONVERTA,2")
    revConvertFU1 = ReceivePLCCmd("CONVERTB,1", "00000,00000,00000,00000,CONVERTB,1")
    revConvertFU2 = ReceivePLCCmd("CONVERTB,2", "00000,00000,00000,00000,CONVERTB,2")


    # calibrate offset value
    sendStartCaliRU = "00000,00000,00000,00000,CALIA,1,"
    sendChangeCaliRU = "{},{},{},{},CALIA,2,"
    sendDoneCaliRU = "00000,00000,00000,00000,CALIA,D,"

    sendStartCaliFU = "00000,00000,00000,00000,CALIB,1,"
    sendChangeCaliFU = "{},{},{},{},CALIB,2,"
    sendDoneCaliFU = "00000,00000,00000,00000,CALIB,D,"

    revStartCaliRU = ReceivePLCCmd("CALIA,1", "00000,00000,00000,00000,CALIA,1")
    revChangeCaliRU = ReceivePLCCmd("CALIA,2", "00000,00000,00000,00000,CALIA,2")
    revStartCaliFU = ReceivePLCCmd("CALIB,1", "00000,00000,00000,00000,CALIB,1")
    revChangeCaliFU = ReceivePLCCmd("CALIB,2", "00000,00000,00000,00000,CALIB,2")

    # get offset value
    sendGetOffsetRU = "00000,00000,00000,00000,OFFSETA,1,"
    sendGetOffsetFU = "00000,00000,00000,00000,OFFSETB,1,"

    sendGetOffset = "00000,00000,00000,00000,OFFSET,1,"

    revGetOffset = ReceivePLCCmd("OFFSET,1", "00000,00000,00000,00000,OFFSET,1")
    revGetOffsetRU = ReceivePLCCmd("OFFSETA,1", "00000,00000,00000,00000,OFFSETA,1")
    revGetOffsetFU = ReceivePLCCmd("OFFSETA,1", "00000,00000,00000,00000,OFFSETB,1")

    # auto
    revReady = ReceivePLCCmd("READY,","00000000000,READY")
    sendReady = "00000,00000,00000,00000,READY,"

    revRequestTrigRU1 = ReceivePLCCmd("TRIGRA,2", "00000,00000,00000,00000,TRIGRA,2")
    revDoneTrigRU1 = ReceivePLCCmd("TRIGDA,2", "00000,00000,00000,00000,TRIGDA,2")
    sendRequestTrigRU1 = "{},{},{},{},TRIGRA,2,"

    revRequestTrigRU2 = ReceivePLCCmd("TRIGRA,1", "00000,00000,00000,00000,TRIGRA,1")
    revDoneTrigRU2 = ReceivePLCCmd("TRIGDA,1", "00000,00000,00000,00000,TRIGDA,1")
    sendRequestTrigRU2 = "{},{},{},{},TRIGRA,1,"

    revRequestTrigFU1 = ReceivePLCCmd("TRIGRB,2", "00000,00000,00000,00000,TRIGRB,2")
    revDoneTrigFU1 = ReceivePLCCmd("TRIGDB,2", "00000,00000,00000,00000,TRIGDB,2")
    sendRequestTrigFU1 = "{},{},{},{},TRIGRB,2,"

    revRequestTrigFU2 = ReceivePLCCmd("TRIGRB,1", "00000,00000,00000,00000,TRIGRB,1")
    revDoneTrigFU2 = ReceivePLCCmd("TRIGDB,1", "00000,00000,00000,00000,TRIGDB,1")
    sendRequestTrigFU2 = "{},{},{},{},TRIGRB,1,"

    revRequestTrigFU3 = ReceivePLCCmd("TRIGRB,3", "00000,00000,00000,00000,TRIGRB,3")
    revDoneTrigFU3 = ReceivePLCCmd("TRIGDB,3", "00000,00000,00000,00000,TRIGDB,3")
    sendRequestTrigFU3 = "{},{},{},{},TRIGRB,3,"

    revRequestGrip = ReceivePLCCmd("GRIPR,1,", "00000,00000,00000,00000,GRIPR,1,")
    sendRequestGrip = "{},{},{},{},GRIPR,1,"


    sendTrigOk = "00000,00000,00000,00000,TRIG,OK,"
    sendTrigNG = "00000,00000,00000,00000,TRIG,NG,"

class ReceivePLCCmdWithComma:
    signal = ""
    numOfComma = 0

    def __init__(self, signal, numOfComma = 0):
        self.signal = signal
        self.numOfComma = numOfComma

    def getDataWithComma(self, plcData):
        try:
            recvData = str(plcData).replace("\x00", "")
            dataList = recvData.split(",")

            signalIndex = dataList.index(self.signal)
            endIndex = signalIndex + self.numOfComma + 1

            finalData = dataList[signalIndex : endIndex]

            return finalData
        except Exception as error:
            print("ERROR Get data with Comma: {}".format(error))

    def getDataWithCR(self, plcData):
        data = str(plcData).replace("\x00", "")
        dataList = data.split(",CR")
        for data in dataList:
            if data.__contains__(self.signal):
                return data
        return ""
    
    def getDataWithSemicolon(self, plcData):
        data = str(plcData).replace("\x00", "")
        dataList = data.split(";")
        for data in dataList:
            if data.__contains__(self.signal):
                return data
        return ""

    def getDataWithSquareBrackets(self, plcData):
        data = str(plcData).replace("\x00", "")
        dataList = data.split("[")
        for data in dataList:
            if data.__contains__(self.signal):
                return data
        return ""

class Roto_Weighing_Cmd(enum.Enum):
    sendCaliOffset = "CALI_OFFSET,{},{},CR"
    revCaliOffset = ReceivePLCCmdWithComma("CALI_OFFSET", 3) # CALI_OFFSET, x, y, cr
    sendCaliDone = "CALI_DONE,CR"

    sendGetOffset = "GET_OFFSET,CR"
    revGetOffset = ReceivePLCCmdWithComma("GET_OFFSET", 3) # GET_OFFSET, x, y, cr

    revTakePicPoint1 = ReceivePLCCmdWithComma("TAKE_PIC_1", 3) # TAKE_PIC_1, x, y, cr
    revTakePicPoint2 = ReceivePLCCmdWithComma("TAKE_PIC_2", 3) # TAKE_PIC_2, x, y, cr

    send_OK_Deviation = "OK,{}"
    send_NG_Deviation = "NG,{},{},CR"

class DDK_INSPECTION_CMD(enum.Enum):
    # read
    p_motion_ready = ReceivePLCCmdWithComma(signal="MotionReady", numOfComma=0) # [STATION1;STEP1;MotionReady;0;0;0;0;0;0;0]
    p_plc_trigger = ReceivePLCCmdWithComma(signal="Trigger", numOfComma=0) # [STATION1;STEP1;Trigger;0;0;0;0;0;0;0]
    p_get_result = ReceivePLCCmdWithComma(signal="GetResult", numOfComma=0) # [STATION1;STEP1;GetResult;0;0;0;0;0;0;0]
    p_reset_process = ReceivePLCCmdWithComma(signal="ResetProcess", numOfComma=0) # [STATION1;STEP1;GetResult;0;0;0;0;0;0;0]
    p_moving_done = ReceivePLCCmdWithComma(signal="MovingDone", numOfComma=0) # [STATION1;STEP1;MovingDone;0;0;0;0;0;0;0]
    p_reset_done = ReceivePLCCmdWithComma(signal="ResetDone", numOfComma=0) # [STATION1;STEP1;ResetDone;0;0;0;0;0;0;0]
    # send
    v_trigger_ready = "[Station{};Step{};TriggerReady;0;0;0;0;0;0;0]"
    v_trigger_busy = "[Station{};Step{};TriggerBusy;0;0;0;0;0;0;0]"
    v_image_ready = "[Station{};Step{};ImageReady;0;0;0;0;0;0;0]"
    v_image_not_ready = "[Station{};Step{};ImageNotReady;0;0;0;0;0;0;0]"
    v_image_again = "[Station{};Step{};ImageAgain;0;0;0;0;0;0;0]"
    v_image_failed = "[Station{};Step{};ImageFailed;0;0;0;0;0;0;0]"
    v_processing = "[Station{};Step{};Processing;0;0;0;0;0;0;0]"
    v_process_done = "[Station{};Step{};ProcessDone;{};{};0;0;0;0;0]"
    v_reset_done = "[Station{};Step{};ResetDone;0;0;0;0;0;0;0]"
    v_request_moving = "[Station{};Step{};RequestMoving;0;0;0;0;0;0;0]"
    v_request_reset_process = "[Station{};Step{};ResetProcess;0;0;0;0;0;0;0]"

class Common_Cmd(enum.Enum):
    send_NG = "NG,{}" # NG, error
