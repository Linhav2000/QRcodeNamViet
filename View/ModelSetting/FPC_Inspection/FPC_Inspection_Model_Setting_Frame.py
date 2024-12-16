from Modules.ModelSetting.ModelParameter import ModelParameter
from View.Common.CommonStepFrame import *
from View.Common.VisionUI import *
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from Modules.ModelSetting.Algorithm_Choose import Algorithm_Choose
from CommonAssit import PathFileControl
from CommonAssit import TimeControl
import cv2 as cv

class FPC_Inspection_Model_Setting_Frame(VisionLabelFrame):

    yDistance = 35
    xDistance = 150

    findContoursFrame: VisionFrame
    minContoursArea: InputParamFrame
    maxContoursArea: InputParamFrame
    minContoursWidth: InputParamFrame
    maxContoursWidth: InputParamFrame
    minContoursHeight: InputParamFrame
    maxContoursHeight: InputParamFrame
    numContourThresh: InputParamFrame

    rotate_algorithm: Algorithm_Choose
    translation_algorithm: Algorithm_Choose
    inspection_algorithm: Algorithm_Choose
    position_detect_algorithm: Algorithm_Choose

    inspection_camera: ComboForFlexibleValue
    position_camera: ComboForFlexibleValue

    height_checking: InputParamFrame
    brightness_reflection_1: InputParamFrame
    brightness_reflection_2: InputParamFrame
    fpc_type: InputParamFrame

    btn_get_reference_parameter: VisionButton
    top_vertical_y: InputParamFrame
    bottom_vertical_y: InputParamFrame
    left_horizontal_x: InputParamFrame
    right_horizontal_x: InputParamFrame
    rear_distance: InputParamFrame

    horizontal_line = []
    vertical_line = []
    base_point = []
    base_roi_path = ""

    def __init__(self, master, text=""):
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        VisionLabelFrame.__init__(self, master, text=text)
        self.modelSettingTab: ModelSettingTab = master
        self.mainWindow = self.modelSettingTab.mainWindow
        self.parameter = ModelParameter()
        self.setupView()

    def updateValue(self, parameter: ModelParameter):
        self.parameter = parameter
        self.rotate_algorithm.setStringValue(parameter.fi_rotate_algorithm)
        self.translation_algorithm.setStringValue(parameter.fi_translation_algorithm)
        self.inspection_algorithm.setStringValue(parameter.fi_inspection_algorithm)
        self.position_detect_algorithm.setStringValue(parameter.fi_position_detect_algorithm)
        self.inspection_camera.setPosValue(parameter.fi_inspection_camera)
        self.position_camera.setPosValue(parameter.fi_position_camera)
        self.height_checking.setValue(parameter.fi_height_checking)
        self.horizontal_line = parameter.fi_reference_line_horizontal
        self.vertical_line = parameter.fi_reference_line_vertical
        self.base_point = parameter.fi_reference_base_point
        self.base_roi_path = parameter.fi_base_roi_path
        self.fpc_type.setValue(parameter.fi_fpc_type)
        self.brightness_reflection_1.setValue(parameter.fi_brightness_reflection_1)
        self.brightness_reflection_2.setValue(parameter.fi_brightness_reflection_2)
        self.top_vertical_y.setValue(parameter.fi_top_vertical_y)
        self.bottom_vertical_y.setValue(parameter.fi_bottom_vertical_y)
        self.left_horizontal_x.setValue(parameter.fi_left_horizontal_x)
        self.right_horizontal_x.setValue(parameter.fi_right_horizontal_x)
        self.rear_distance.setValue(parameter.fi_rear_distance)

    def save(self, model: ModelParameter):
        model.fi_rotate_algorithm = self.rotate_algorithm.getValue()
        model.fi_translation_algorithm = self.translation_algorithm.getValue()
        model.fi_inspection_algorithm = self.inspection_algorithm.getValue()
        model.fi_position_detect_algorithm = self.position_detect_algorithm.getValue()
        model.fi_inspection_camera = self.inspection_camera.getPosValue()
        model.fi_position_camera = self.position_camera.getPosValue()
        model.fi_height_checking = self.height_checking.getIntValue()
        model.fi_reference_line_horizontal = self.horizontal_line
        model.fi_reference_line_vertical = self.vertical_line
        model.fi_reference_base_point = self.base_point
        model.fi_base_roi_path = self.base_roi_path
        model.fi_fpc_type = self.fpc_type.getIntValue()
        model.fi_brightness_reflection_1 = self.brightness_reflection_1.getIntValue()
        model.fi_brightness_reflection_2 = self.brightness_reflection_2.getIntValue()
        model.fi_top_vertical_y = self.top_vertical_y.getIntValue()
        model.fi_bottom_vertical_y = self.bottom_vertical_y.getIntValue()
        model.fi_rear_distance = self.rear_distance.getIntValue()
        model.fi_left_horizontal_x = self.left_horizontal_x.getIntValue()
        model.fi_right_horizontal_x = self.right_horizontal_x.getIntValue()
        return model

    def isChanged(self, model: ModelParameter):
        ret =  model.fi_rotate_algorithm != self.rotate_algorithm.getValue()
        ret = ret or model.fi_translation_algorithm != self.translation_algorithm.getValue()
        ret = ret or model.fi_inspection_algorithm != self.inspection_algorithm.getValue()
        ret = ret or model.fi_position_detect_algorithm != self.position_detect_algorithm.getValue()
        ret = ret or model.fi_position_camera != self.position_camera.getPosValue()
        ret = ret or model.fi_inspection_camera != self.inspection_camera.getPosValue()
        ret = ret or model.fi_height_checking != self.height_checking.getIntValue()
        ret = ret or model.fi_reference_line_horizontal != self.horizontal_line
        ret = ret or model.fi_reference_line_vertical != self.vertical_line
        ret = ret or model.fi_reference_base_point != self.base_point
        ret = ret or model.fi_base_roi_path != self.base_roi_path
        ret = ret or model.fi_fpc_type != self.fpc_type.getIntValue()
        ret = ret or model.fi_brightness_reflection_1 != self.brightness_reflection_1.getIntValue()
        ret = ret or model.fi_brightness_reflection_2 != self.brightness_reflection_2.getIntValue()
        ret = ret or model.fi_top_vertical_y != self.top_vertical_y.getIntValue()
        ret = ret or model.fi_bottom_vertical_y != self.bottom_vertical_y.getIntValue()
        ret = ret or model.fi_left_horizontal_x != self.left_horizontal_x.getIntValue()
        ret = ret or model.fi_right_horizontal_x != self.right_horizontal_x.getIntValue()
        ret = ret or model.fi_rear_distance != self.rear_distance.getIntValue()
        return ret

    def setupView(self):
        algorithmList = [algorithm.algorithmParameter.name for algorithm in
                         self.mainWindow.algorithmManager.algorithmList]
        self.rotate_algorithm = Algorithm_Choose(self, "Rotate Algorithm: ", yPos= 0* self.yDistance + 5,
                                                height=self.yDistance, valueList=algorithmList,
                                                 mainWindow=self.mainWindow,
                                                 add_new_done_cmd=self.updateAlgorithmList)

        self.translation_algorithm = Algorithm_Choose(self, "Translation Algorithm: ", yPos=1 * self.yDistance + 5,
                                                      height=self.yDistance, valueList=algorithmList,
                                                      mainWindow=self.mainWindow,
                                                      add_new_done_cmd=self.updateAlgorithmList)

        self.inspection_algorithm = Algorithm_Choose(self, "Inspection Algorithm: ", yPos=2 * self.yDistance + 5,
                                                      height=self.yDistance, valueList=algorithmList,
                                                      mainWindow=self.mainWindow,
                                                      add_new_done_cmd=self.updateAlgorithmList)

        self.position_detect_algorithm = Algorithm_Choose(self, "Pos Detect Algorithm: ", yPos=3 * self.yDistance + 5,
                                                            height=self.yDistance, valueList=algorithmList,
                                                      mainWindow=self.mainWindow,
                                                      add_new_done_cmd=self.updateAlgorithmList)

        camera_name_list = []
        for i in range(10):
            camera_name_list.append(f"Camera {i}")

        self.inspection_camera = ComboForFlexibleValue(self, "Inspection camera:", yPos=4 * self.yDistance + 5,
                                                       height=self.yDistance, valueList=camera_name_list)

        self.position_camera = ComboForFlexibleValue(self, "Position camera:", yPos=5 * self.yDistance + 5,
                                              height=self.yDistance, valueList=camera_name_list)

        self.height_checking = InputParamFrame(self, "Height checking: ", 6 * self.yDistance + 5, self.yDistance)
        self.fpc_type = InputParamFrame(self, "FPC Type: ", 7 * self.yDistance + 5, self.yDistance)

        self.top_vertical_y = InputParamFrame(self, "Top vertical Y : ", 8 * self.yDistance + 5, self.yDistance)
        self.bottom_vertical_y = InputParamFrame(self, "Bottom vertical Y : ", 9 * self.yDistance + 5, self.yDistance)

        self.left_horizontal_x = InputParamFrame(self, "Left horizontal X: ", 10 * self.yDistance + 5, self.yDistance)
        self.right_horizontal_x = InputParamFrame(self, "Right horizontal X: ", 11 * self.yDistance + 5, self.yDistance)

        self.brightness_reflection_1 = InputParamFrame(self, "Brightness reflection 1: ", 12 * self.yDistance + 5, self.yDistance)
        self.brightness_reflection_2 = InputParamFrame(self, "Brightness reflection 2: ", 13 * self.yDistance + 5, self.yDistance)
        self.rear_distance = InputParamFrame(self, "Rear distance: ", 14 * self.yDistance + 5, self.yDistance)

        self.btn_get_reference_parameter = VisionButton(self, text="Take reference parameter", command=self.click_btn_get_reference_parm)
        self.btn_get_reference_parameter.place(x=5, y=15 * self.yDistance + 5, height=30)

    def click_btn_get_reference_parm(self):
        self.mainWindow.workingThread.create_fpc_inspection()
        self.mainWindow.workingThread.fpc_inspection.updateModel()
        sourceImage = self.mainWindow.originalImage.copy()
        verticalLine, horizontal_line, base_point, base_roi = self.mainWindow.workingThread.fpc_inspection.imageProcessThread(sourceImage, 0, isSetting=True)
        self.horizontal_line = horizontal_line
        self.vertical_line = verticalLine
        self.base_point = base_point
        if base_roi is not None:
            PathFileControl.generatePath("./config/resource")
            base_roi_path = f"./config/resource/fpc_base_roi_{TimeControl.y_m_d_H_M_S_format()}.bmp"
            cv.imencode(".bmp", base_roi)[1].tofile(base_roi_path)
            # cv.imwrite(base_roi_path, base_roi)
            self.base_roi_path = base_roi_path



    def updateAlgorithmList(self):
        algorithmList = [algorithm.algorithmParameter.name for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList]
        self.rotate_algorithm.updateValueList(algorithmList)
        self.translation_algorithm.updateValueList(algorithmList)
        self.inspection_algorithm.updateValueList(algorithmList)
        self.position_detect_algorithm.updateValueList(algorithmList)