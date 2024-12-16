from tkinter import messagebox
from Modules.ModelSetting.NumOfRefPoint import NumOfRefPoint
from Modules.ModelSetting.CAS_Type import CAS_Type
from ImageProcess.Algorithm.MethodList import MethodList

class ModelParameter:
    name = "model"
    plcRef1Pos = (0, 0, 0)
    refPoint1 = (0, 0)
    refPoint2 = (0, 0)
    refPoint3 = (0, 0)
    offsetPoint = (0, 0)
    offset = (0, 0, 0)
    conversionCoef = 1
    designFilePath = ""
    activeFrom = 0
    activeTo = 0
    activePointsSetting = []
    numOfRefPoint = NumOfRefPoint._3RefPoint.value

    # Rear missing parameter:
    leftCameraId = 0
    rightCameraId = 1
    leftAlgorithm = ""
    rightAlgorithm = ""

    threshValue = 200
    screwRecognizeAlgorithm = ""
    ringRecognizeAlgorithm = ""
    centerHoleAlgorithm = ""
    boltRadius = 300
    minDist = 1
    parm1 = 100
    parm2 = 50


    # Fu assembly parameter
    ruCameraId = 0
    fuCameraId = 0
    ruAlgorithm = ""
    fuAlgorithm = ""
    ruLightId = 0
    fuLightId = 0

    ruRef1Design = (0, 0)
    ruRef2Design = (0, 0)
    fuRef1Design = (0, 0)
    fuRef2Design = (0, 0)
    plcRuRef1Pos = (0, 0, 0, 0)
    plcRuRef2Pos = (0, 0, 0, 0)
    plcFuRef1Pos = (0, 0, 0, 0)
    plcFuRef2Pos = (0, 0, 0, 0)

    plcRuCali = (0, 0, 0, 0)
    plcFuCali = (0, 0, 0, 0)

    ruConversionCoef = 1
    fuConversionCoef = 1

    # detect location

    detectLocationAlgorithm = ""
    demo_location_algorithm = ""
    demo_color_detect_algorithm = ""
    demo_location_thread = ""
    # roto weighing
    rotoAlgorithmStep0 = ""
    rotoAlgorithmStep1 = ""
    roto_weighing_detect_mode = "Tìm tâm"
    casType = CAS_Type.robot_x_pos_y_pos.value
    robot_pixel_mm_Scale_1 = 1
    robot_pixel_mm_Scale_2 = 1
    robot_mm_moving_Scale = 1
    delayTakepicTime = 200
    exceptDelta = 10
    robotOffset_1 = (0, 0)
    robotOffset_2 = (0, 0)
    rw_multiPoint = False

    # fpc inspection
    fi_minArea = -1
    fi_maxArea = -1
    fi_minWidth = -1
    fi_maxWidth = -1
    fi_minHeight = -1
    fi_maxHeight = -1
    fi_count = -1
    fi_rotate_algorithm = ""
    fi_translation_algorithm = ""
    fi_inspection_algorithm = ""
    fi_position_detect_algorithm = ""
    fi_inspection_camera = 0
    fi_position_camera = 1
    fi_height_checking = 1
    fi_reference_line_horizontal = []
    fi_reference_line_vertical = []
    fi_reference_base_point = []
    fi_base_roi_path = ""
    fi_fpc_type = 1
    fi_brightness_reflection_1 = 0
    fi_brightness_reflection_2 = 0
    fi_top_vertical_y = 1
    fi_bottom_vertical_y = 1
    fi_left_horizontal_x = 1
    fi_right_horizontal_x = 1
    fi_rear_distance = 1

    # emap checking
    emap_model_code = ""
    emap_rows = 1
    emap_cols = 1
    emap_distanceX = 1
    emap_distanceY = 1
    emap_start_point = (0, 0)
    emap_size_rect = (1, 1)
    emap_ng_finding_algorithm = ""
    emap_code_reading_algorithm = ""
    emap_ng_finding_camera_id = 0
    emap_code_reading_camera_id = 0

    # tsukuba Housing connector packing
    thcp_rows = 1
    thcp_cols = 1
    thcp_distanceX = 1
    thcp_distanceY = 1
    thcp_start_point = (0, 0)
    thcp_size_rect = (1, 1)
    thcp_ng_finding_algorithm = ""

    # Read weighing
    rw_center = (0, 0)
    rw_start_point = (0, 0)
    rw_end_point = (0, 0)
    rw_start_value = 0
    rw_end_value = 100
    rw_finger_finding_algorithm = ""

    # counting in conveyor

    cic_find_object_algorithm = ''
    cic_in_boundary = 0
    cic_out_boundary = 0
    cic_counting_boundary = 0
    cic_max_disappeared = 1
    cic_max_distance = 10
    cic_bip = 0

    #DDK
    ddk_origin_algorithm  = ""
    ddk_algorithm_list  = ["0","1","2","3","4","5","6","7","8","9","0","1","2","3","4","5","6","7","8","9"]
    save_ng_image = (False, "jpg", "./data/DDK/saveImage/NG", "None")
    save_ok_image = (False, "jpg", "./data/DDK/saveImage/OK", "None")
    ddk_num_of_step = 20

    #SYC
    syc_algorithm_list = ["0","1","2"]
    syc_save_NG_image = (False, "jpg", "./data/SYC/Images/NG", "None")
    syc_save_OK_image = (False, "jpg", "./data/SYC/Images/OK", "None")
    syc_hardware_trigger = False
    syc_model_update = ""

    # Washing machine inspection
    wmi_use_hardware_trigger = False
    wmi_camera_1_id = 0

    def makeStandardType(self):
        self.plcRef1Pos = (int(self.plcRef1Pos[0]), int(self.plcRef1Pos[1]), int(self.plcRef1Pos[2]))
        self.refPoint1 = (float(self.refPoint1[0]), float(self.refPoint1[1]))
        self.refPoint2 = (float(self.refPoint2[0]), float(self.refPoint2[1]))
        self.refPoint3 = (float(self.refPoint3[0]), float(self.refPoint3[1]))
        self.offsetPoint = (float(self.offsetPoint[0]), float(self.offsetPoint[1]))
        self.offset = (int(float(self.offset[0])), int(float(self.offset[1])), int(float(self.offset[2])))
        self.conversionCoef = float(self.conversionCoef)
        self.activeFrom = int(float(self.activeFrom))
        self.activeTo = int(float(self.activeTo))
        self.threshValue = int(float(self.threshValue))
        self.boltRadius = int(float(self.boltRadius))
        self.parm1 = int(self.parm1)
        self.parm2 = int(self.parm2)
        self.minDist = int(self.minDist)

    def isReadyForRunning(self):
        ret = True

        if self.refPoint1[0] == 0 or self.refPoint1[1] == 0 \
           or self.refPoint2[0] == 0 or self.refPoint2[1] == 0 \
           or self.refPoint3[0] == 0 or self.refPoint3[1] == 0:
            messagebox.showerror("Model Setting", "This model still not set the REFERENCE POSITION\nPlease select enough 3 reference positions!")
            ret = False

        if self.offsetPoint[0] == 0 or self.offsetPoint[1] == 0:
            messagebox.showerror("Model Setting", "This model still not set the OFFSET POINT\nPlease select OFFSET POINT!")
            ret = False
        if self.plcRef1Pos[0] == 0 or self.plcRef1Pos[1] == 0 or self.plcRef1Pos[2] == 0 \
           or (self.offset[0] == 0 and self.offset[1] == 0 and self.offset[2] == 0):
            messagebox.showerror("Model Setting", "This model still not calibrate\nPlease take conversion coefficient and calibrate offset!")
            ret = False

        if self.designFilePath == "":
            messagebox.showerror("Model Setting", "Still not setting Design file path for this model\nPlease set in model setting tab!")
            ret = False

        return ret
