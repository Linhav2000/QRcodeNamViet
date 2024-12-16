from View.Common.CommonStepFrame import *
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from CommonAssit.CommunicationReceiveAnalyze import DDK_parameter
from View.Common.ScrollFrame import ScrollView
from CommonAssit.DDK_CONSTANT import *

class DDK_Manual_Parameter:
    station = 1
    step = 1
    client_capture_passed = False  # 1-Pass/0-Fail
    client_process_passed = False  # 1-Pass/0-Fail
    client_step_tact_time = 0
    client_image_error_code = 0
    client_sw_error_code = 0
    host_request_reset = False  # 0-None/1-Request
    client_request_reset = False  # 0-None/1-Request
    host_motion_ready_flag = True  # 0-Not Yet/1-Already
    client_vision_ready_flag = False  # 0-Not Yet/1-Already
    host_auto_request = True  # 0-Auto/1-Manual
    client_auto_request = False  # 0-Auto/1-Manual
    client_step_finish = False  # 0-None/1-Finish
    host_auto_flag = True  # 0-Auto/1-Manual
    client_manual_go = False  # 0-Auto/1-Manual
    host_read_flag = True  # 0-Ready/1-Write
    real_time = 0  # to save image name

class DDK_Manual_Signal_Frame(VisionFrame):
    yDistance = 30
    ddk_manual_parameter: DDK_Manual_Parameter
    mode: ComboForFlexibleValue
    station_no: InputParamFrame
    step_no: InputParamFrame
    client_capture_passed: CheckboxStepParamFrame
    client_process_passed: CheckboxStepParamFrame
    client_step_tact_time: InputParamFrame
    client_image_error_code: InputParamFrame
    client_sw_error_code: InputParamFrame
    host_request_reset: CheckboxStepParamFrame
    host_request_reset: CheckboxStepParamFrame
    host_motion_ready_flag: CheckboxStepParamFrame
    client_vision_ready_flag: CheckboxStepParamFrame
    host_auto_request: CheckboxStepParamFrame
    client_request_reset: CheckboxStepParamFrame
    host_auto_request: CheckboxStepParamFrame
    client_auto_request: CheckboxStepParamFrame
    client_step_finish: CheckboxStepParamFrame
    host_auto_flag: CheckboxStepParamFrame
    client_manual_go: CheckboxStepParamFrame
    host_read_flag: CheckboxStepParamFrame
    real_time: InputParamFrame
    scrollView: ScrollView
    def __init__(self, master):
        VisionFrame.__init__(self, master)
        self.ddk_manual_parameter = DDK_Manual_Parameter()
        self.setupView()
        self.setValue()

    def setupView(self):
        mode_list = ("Display", "Control")
        self.mode = ComboForFlexibleValue(self, "Mode :", yPos=10 + 0*self.yDistance, height=self.yDistance,
                                          combo_width=100, xDistance=150, valueList=mode_list)
        self.mode.setPosValue(0)

        self.scrollView = ScrollView(self, displayHeight=1000, borderwidth=0)
        self.scrollView.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

        self.station_no = InputParamFrame(self.scrollView.display, "Station :", yPos=10 + 0*self.yDistance, height=self.yDistance)
        self.step_no = InputParamFrame(self.scrollView.display, "Step :", yPos=10 + 1*self.yDistance, height=self.yDistance)
        self.client_capture_passed = CheckboxStepParamFrame(self.scrollView.display, "Capture passed/failed :", yPos=10 + 2 * self.yDistance, height=self.yDistance, xDistance=250)
        self.client_process_passed = CheckboxStepParamFrame(self.scrollView.display, "Client process passed/failed :", yPos=10 + 3 * self.yDistance, height=self.yDistance, xDistance=250)
        self.client_step_tact_time = InputParamFrame(self.scrollView.display, "Tact time :", yPos=10 + 4*self.yDistance, height=self.yDistance)
        self.client_image_error_code = InputParamFrame(self.scrollView.display, "Image error code :", yPos=10 + 5*self.yDistance, height=self.yDistance)
        self.client_sw_error_code = InputParamFrame(self.scrollView.display, "SW error code :", yPos=10 + 6*self.yDistance, height=self.yDistance)
        self.host_request_reset = CheckboxStepParamFrame(self.scrollView.display, "Host request reset :", yPos=10 + 7*self.yDistance, height=self.yDistance, xDistance=250)
        self.client_request_reset = CheckboxStepParamFrame(self.scrollView.display, "Client request reset :", yPos=10 + 8*self.yDistance, height=self.yDistance, xDistance=250)
        self.host_motion_ready_flag = CheckboxStepParamFrame(self.scrollView.display, "Host motion ready/not :", yPos=10 + 9*self.yDistance, height=self.yDistance, xDistance=250)
        self.client_vision_ready_flag = CheckboxStepParamFrame(self.scrollView.display, "Client ready/not flag :", yPos=10 + 10*self.yDistance, height=self.yDistance, xDistance=250)
        self.host_auto_request = CheckboxStepParamFrame(self.scrollView.display, "Host auto request :", yPos=10 + 11*self.yDistance, height=self.yDistance, xDistance=250)
        self.client_auto_request = CheckboxStepParamFrame(self.scrollView.display, "Client auto request :", yPos=10 + 12*self.yDistance, height=self.yDistance, xDistance=250)
        self.client_step_finish = CheckboxStepParamFrame(self.scrollView.display, "Client step finish/not :", yPos=10 + 13*self.yDistance, height=self.yDistance, xDistance=250)
        self.host_auto_flag = CheckboxStepParamFrame(self.scrollView.display, "Host auto/manual flag :", yPos=10 + 14*self.yDistance, height=self.yDistance, xDistance=250)
        self.client_manual_go = CheckboxStepParamFrame(self.scrollView.display, "Client manual/auto go :", yPos=10 + 15*self.yDistance, height=self.yDistance, xDistance=250)
        self.host_read_flag = CheckboxStepParamFrame(self.scrollView.display, "Host read/write flag :", yPos=10 + 16*self.yDistance, height=self.yDistance, xDistance=250)
        self.real_time = InputParamFrame(self.scrollView.display, "Time :", yPos=10 + 17*self.yDistance, height=self.yDistance)

    def setValue(self, ddk_parameter: DDK_parameter=None):
        if ddk_parameter is not None:
            self.convert_parameter(ddk_parameter)

        self.station_no.setValue(self.ddk_manual_parameter.station)
        self.step_no.setValue(self.ddk_manual_parameter.step)
        self.client_capture_passed.setValue(self.ddk_manual_parameter.client_capture_passed)
        self.client_process_passed.setValue(self.ddk_manual_parameter.client_process_passed)
        self.client_step_tact_time.setValue(self.ddk_manual_parameter.client_step_tact_time)
        self.client_image_error_code.setValue(self.ddk_manual_parameter.client_image_error_code)
        self.client_sw_error_code.setValue(self.ddk_manual_parameter.client_sw_error_code)
        self.host_request_reset.setValue(self.ddk_manual_parameter.host_request_reset)
        self.client_request_reset.setValue(self.ddk_manual_parameter.client_request_reset)
        self.host_motion_ready_flag.setValue(self.ddk_manual_parameter.host_motion_ready_flag)
        self.client_vision_ready_flag.setValue(self.ddk_manual_parameter.client_vision_ready_flag)
        self.host_auto_request.setValue(self.ddk_manual_parameter.host_auto_request)
        self.client_auto_request.setValue(self.ddk_manual_parameter.client_auto_request)
        self.client_step_finish.setValue(self.ddk_manual_parameter.client_step_finish)
        self.host_auto_flag.setValue(self.ddk_manual_parameter.host_auto_flag)
        self.client_manual_go.setValue(self.ddk_manual_parameter.client_manual_go)
        self.host_read_flag.setValue(self.ddk_manual_parameter.host_read_flag)
        self.real_time.setValue(self.ddk_manual_parameter.real_time)

    def getValue(self, ddk_parameter: DDK_parameter):
        if self.mode.getValue() == "Display":
            return ddk_parameter
        self.ddk_manual_parameter.station = self.station_no.getIntValue()
        self.ddk_manual_parameter.step = self.step_no.getIntValue()
        self.ddk_manual_parameter.client_capture_passed = self.client_capture_passed.getValue()
        self.ddk_manual_parameter.client_process_passed = self.client_process_passed.getValue()
        self.ddk_manual_parameter.client_step_tact_time = self.client_step_tact_time.getIntValue()
        self.ddk_manual_parameter.client_image_error_code = self.client_image_error_code.getIntValue()
        self.ddk_manual_parameter.client_sw_error_code = self.client_sw_error_code.getIntValue()
        self.ddk_manual_parameter.host_request_reset = self.host_request_reset.getValue()
        self.ddk_manual_parameter.client_request_reset = self.client_request_reset.getValue()
        self.ddk_manual_parameter.host_motion_ready_flag = self.host_motion_ready_flag.getValue()
        self.ddk_manual_parameter.client_vision_ready_flag = self.client_vision_ready_flag.getValue()
        self.ddk_manual_parameter.host_auto_request = self.host_auto_request.getValue()
        self.ddk_manual_parameter.client_auto_request = self.client_auto_request.getValue()
        self.ddk_manual_parameter.client_step_finish = self.client_step_finish.getValue()
        self.ddk_manual_parameter.host_auto_flag = self.host_auto_flag.getValue()
        self.ddk_manual_parameter.client_manual_go = self.client_manual_go.getValue()
        self.ddk_manual_parameter.host_read_flag = self.host_read_flag.getValue()
        self.ddk_manual_parameter.real_time = self.real_time.getValue()
        return self.revert_parameter()

    def convert_parameter(self, ddk_parameter: DDK_parameter):
        self.ddk_manual_parameter.station = ddk_parameter.station
        self.ddk_manual_parameter.step = ddk_parameter.step
        self.ddk_manual_parameter.client_capture_passed = True if ddk_parameter.client_capture_result == PASSED else False
        self.ddk_manual_parameter.client_process_passed = True if ddk_parameter.client_process_result == PASSED else False
        self.ddk_manual_parameter.client_step_tact_time = ddk_parameter.client_step_tact_time
        self.ddk_manual_parameter.client_image_error_code = ddk_parameter.client_image_error_code
        self.ddk_manual_parameter.client_sw_error_code = ddk_parameter.client_sw_error_code
        self.ddk_manual_parameter.host_request_reset = True if ddk_parameter.host_request_reset == REQUEST else False  # 0-None/1-Request
        self.ddk_manual_parameter.client_request_reset = True if ddk_parameter.client_request_reset == REQUEST else False  # 0-None/1-Request
        self.ddk_manual_parameter.host_motion_ready_flag = True if ddk_parameter.host_motion_ready_flag == READY else False  # 0-Not Yet/1-Already
        self.ddk_manual_parameter.client_vision_ready_flag = True if ddk_parameter.client_vision_ready_flag == READY else False  # 0-Not Yet/1-Already
        self.ddk_manual_parameter.host_auto_request = True if ddk_parameter.host_auto_request == REQUEST else False
        self.ddk_manual_parameter.client_auto_request = True if ddk_parameter.client_auto_request == REQUEST else False  # 0-Auto/1-Manual
        self.ddk_manual_parameter.client_step_finish = True if ddk_parameter.client_step_finish == FINISH else False  # 0-None/1-Finish
        self.ddk_manual_parameter.host_auto_flag = True if ddk_parameter.host_auto_flag == AUTO else False  # 0-Auto/1-Manual
        self.ddk_manual_parameter.client_manual_go = True if ddk_parameter.client_manual_go == MANUAL else False  # 0-Auto/1-Manual
        self.ddk_manual_parameter.host_read_flag = True if ddk_parameter.host_read_flag == READ else False # 0-Ready/1-Write
        self.ddk_manual_parameter.real_time = ddk_parameter.real_time  # to save image name

    def revert_parameter(self, ddk_parameter: DDK_parameter= None):
        if ddk_parameter is None:
            ddk_parameter = DDK_parameter()
        ddk_parameter.station = self.ddk_manual_parameter.station
        ddk_parameter.step = self.ddk_manual_parameter.step
        ddk_parameter.client_capture_result = PASSED if self.ddk_manual_parameter.client_capture_passed == True else FAILED  # 1-Pass/0-Fail
        ddk_parameter.client_process_result = PASSED if self.ddk_manual_parameter.client_process_passed == True else FAILED  # 1-Pass/0-Fail
        ddk_parameter.client_step_tact_time = self.ddk_manual_parameter.client_step_tact_time
        ddk_parameter.client_image_error_code = self.ddk_manual_parameter.client_image_error_code
        ddk_parameter.client_sw_error_code = self.ddk_manual_parameter.client_sw_error_code
        ddk_parameter.host_request_reset = REQUEST if self.ddk_manual_parameter.host_request_reset else NONE  # 0-None/1-Request
        ddk_parameter.client_request_reset = REQUEST if self.ddk_manual_parameter.client_request_reset else NONE  # 0-None/1-Request
        ddk_parameter.host_motion_ready_flag = READY if self.ddk_manual_parameter.host_motion_ready_flag else NOT_YET  # 0-Not Yet/1-Already
        ddk_parameter.client_vision_ready_flag = READY if self.ddk_manual_parameter.client_vision_ready_flag else NOT_YET  # 0-Not Yet/1-Already
        ddk_parameter.host_auto_request = REQUEST if self.ddk_manual_parameter.host_auto_request else NONE  # 0-Auto/1-Manual
        ddk_parameter.client_auto_request = REQUEST if self.ddk_manual_parameter.client_auto_request else NONE  # 0-Auto/1-Manual
        ddk_parameter.client_step_finish = FINISH if self.ddk_manual_parameter.client_step_finish else NOT_YET  # 0-None/1-Finish
        ddk_parameter.host_auto_flag = AUTO if self.ddk_manual_parameter.host_auto_flag else MANUAL  # 0-Auto/1-Manual
        ddk_parameter.client_manual_go = MANUAL if self.ddk_manual_parameter.client_manual_go else AUTO  # 0-Auto/1-Manual
        ddk_parameter.host_read_flag = READ if self.ddk_manual_parameter.host_read_flag else WRITE  # 0-Ready/1-Write
        ddk_parameter.real_time = self.ddk_manual_parameter.real_time  # to save image name

        return ddk_parameter