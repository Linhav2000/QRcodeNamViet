from tkinter import messagebox
from ImageProcess.Algorithm.MethodList import MethodList
from ImageProcess.Algorithm.StepParamter import *
from ImageProcess import ImageProcess
import cv2 as cv
import numpy as np
from ImageProcess.Algorithm.StepParamter import AdaptiveThreshMode
from ImageProcess.Algorithm.StepParamter import RF_Type, ReferenceEdgeCornerType
from ImageProcess.Algorithm.StepParamter import SourceImageName
from View.Common.CommonStepFrame import *
from Modules.ModelSetting import *
from Modules.ModelSetting.SourceIdxCombo import SourceIdxCombo
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from Modules.ModelSetting.ComboForFixValue import ComboForFixValue
from Modules.ModelSetting.AdjustValueFrame import AdjustValueFrame
from Modules.ModelSetting.SourceInput import SourceInput
import pytesseract

from View.Common.VisionUI import *


class StepSettingFrame(VisionLabelFrame):
    stepParameter: StepParameter

    okButton: OkButton
    exitButton: CancelButton
    btnShowOriginalImage: ShowOriginButton
    btnRemoveWorkingArea: VisionButton
    executeButton: ExecuteButton
    eraseAreaButton: EraseAreaButton
    showAreaButton: ShowAreaButton
    okFlag = False

    resourceImageIndex: SourceInput

    # in range
    bgrToleranceLbl: VisionLabel
    bToleranceLbl: VisionLabel
    gToleranceLbl: VisionLabel
    rToleranceLbl: VisionLabel
    bIRBaseColorEntry: VisionEntry
    gIRBaseColorEntry: VisionEntry
    rIRBaseColorEntry: VisionEntry
    bIRToleranceEntry: VisionEntry
    gIRToleranceEntry: VisionEntry
    rIRToleranceEntry: VisionEntry

    sourceImageLabel: Label
    threshLabel: VisionLabel
    blurSizeLabel: VisionLabel
    cvtColorCodeLabel: VisionLabel

    countNonzeroThreshLbl: VisionLabel
    countNonzeroThreshEntry: VisionEntry

    sourceImageCombobox: ttk.Combobox
    stepList = []
    cvtColorCodeComboBox: ttk.Combobox

    threshEntry: VisionEntry
    blurSizeEntry: VisionEntry
    currentFrame = None

    houghCircleSettingFrame: VisionFrame = None
    inRangeFrame: VisionFrame = None
    countNonzeroFame: VisionFrame = None
    cvtColorFrame: VisionFrame = None
    medianBlurFrame: VisionFrame = None
    matchingTemplateFrame: VisionFrame = None
    colorDetectFrame: VisionFrame = None

    # Contours
    findContoursFrame: VisionFrame = None
    minContoursArea: Slider_Input_Frame
    maxContoursArea: Slider_Input_Frame
    minContoursWidth: Slider_Input_Frame
    maxContoursWidth: Slider_Input_Frame
    minContoursHeight: Slider_Input_Frame
    maxContoursHeight: Slider_Input_Frame
    minAspectRatio: Slider_Input_Frame
    maxAspectRatio: Slider_Input_Frame
    numContourThresh: InputParamFrame
    contours_binarySource: SourceInput
    contours_areaSource: SourceInput

    # erode and dilate
    dilateFrame: VisionFrame = None
    iterations: InputParamFrame
    kernelSizeX: InputParamFrame
    kernelSizeY: InputParamFrame

    # Hough circle
    minDistHoughCircle: Slider_Input_Frame
    parm1HoughCircle: Slider_Input_Frame
    parm2HoughCircle: Slider_Input_Frame
    minRadiusHoughCircle: Slider_Input_Frame
    maxRadiusHoughCircle: Slider_Input_Frame
    betweenDistHoughCircle: Slider_Input_Frame
    trustNumberHoughCircle: InputParamFrame

    # thresh hold
    thresholdFrame: VisionFrame = None
    threshold_thresh_val: Slider_Input_Frame

    maxThresValueEntry: InputParamFrame = None
    threshType1Combo: ComboxBoxStepParmFrame
    threshType2Combo: ComboxBoxStepParmFrame

    # Color detect
    bgrCDToleranceLbl: VisionLabel
    bCDToleranceLbl: VisionLabel
    gCDToleranceLbl: VisionLabel
    rCDToleranceLbl: VisionLabel
    bCDToleranceEntry: VisionEntry
    gCDToleranceEntry: VisionEntry
    rCDToleranceEntry: VisionEntry
    bCDBaseColorEntry: VisionEntry
    gCDBaseColorEntry: VisionEntry
    rCDBaseColorEntry: VisionEntry

    countNonZeroThreshCD: InputParamFrame
    # blur
    blurSize: InputParamFrame
    blurSigmaX: InputParamFrame
    minMatchingValue: InputParamFrame
    multiMatching: CheckboxStepParamFrame
    cvtColorCode: ComboxBoxStepParmFrame
    nonzero_min_range: InputParamFrame
    nonzero_max_range: InputParamFrame

    # adaptive thresh holding
    adaptiveThreshType: ComboForFixValue
    adaptiveChangeVal: InputParamFrame
    adaptiveBlockSize: InputParamFrame
    adaptiveMode: ComboForFixValue
    adaptiveThresholdFrame: VisionFrame = None
    adaptiveThreshMaxVal: InputParamFrame

    # bit wise
    bitwiseFrame: VisionFrame = None
    sourceImage2: SourceIdxCombo
    maskImage: SourceIdxCombo

    # Canny
    cannyFrame: VisionFrame = None
    cannyMinThresh: InputParamFrame
    cannyMaxThresh: InputParamFrame
    canny_kernel_size: InputParamFrame

    # Flip and rotate
    rotateFrame: VisionFrame = None
    rotateCode: ComboForFixValue
    rt_angle: InputParamFrame
    rt_centerX: InputParamFrame
    rt_centerY: InputParamFrame

    flipFrame: VisionFrame = None
    flipCode: ComboForFixValue

    # Original reference
    originalReferenceFrame: VisionFrame = None
    orRef1StepIdx: ComboForFlexibleValue
    orRef2StepIdx: ComboForFlexibleValue
    orRef3StepIdx: ComboForFlexibleValue

    # HLS Range
    hlsRangeFrame: VisionFrame = None
    hlsRangeFrame_HLower: AdjustValueFrame
    hlsRangeFrame_HUpper: AdjustValueFrame
    hlsRangeFrame_LLower: AdjustValueFrame
    hlsRangeFrame_LUpper: AdjustValueFrame
    hlsRangeFrame_SLower: AdjustValueFrame
    hlsRangeFrame_SUpper: AdjustValueFrame
    hls_min_range: InputParamFrame
    hls_max_range: InputParamFrame
    btnShowHLSImage: VisionButton

    # HSV Range
    hsvRangeFrame: VisionFrame = None
    hsvRangeFrame_HLower: AdjustValueFrame
    hsvRangeFrame_HUpper: AdjustValueFrame
    hsvRangeFrame_SLower: AdjustValueFrame
    hsvRangeFrame_SUpper: AdjustValueFrame
    hsvRangeFrame_VLower: AdjustValueFrame
    hsvRangeFrame_VUpper: AdjustValueFrame
    hsv_min_range: InputParamFrame
    hsv_max_range: InputParamFrame
    btnShowHSVImage: VisionButton

    # HSV + HLS range
    hsv_hlsRangeFrame: VisionFrame = None
    hsv_hlsRangeFrame_VHLower: AdjustValueFrame
    hsv_hlsRangeFrame_VHUpper: AdjustValueFrame
    hsv_hlsRangeFrame_VSLower: AdjustValueFrame
    hsv_hlsRangeFrame_VSUpper: AdjustValueFrame
    hsv_hlsRangeFrame_VVLower: AdjustValueFrame
    hsv_hlsRangeFrame_VVUpper: AdjustValueFrame
    hsv_hlsRangeFrame_SHLower: AdjustValueFrame
    hsv_hlsRangeFrame_SHUpper: AdjustValueFrame
    hsv_hlsRangeFrame_SLLower: AdjustValueFrame
    hsv_hlsRangeFrame_SLUpper: AdjustValueFrame
    hsv_hlsRangeFrame_SSLower: AdjustValueFrame
    hsv_hlsRangeFrame_SSUpper: AdjustValueFrame
    hsv_hls_min_range: InputParamFrame
    hsv_hls_max_range: InputParamFrame

    # BGR Range
    bgrRangeFrame: VisionFrame = None
    bgrRangeFrame_BLower: AdjustValueFrame
    bgrRangeFrame_BUpper: AdjustValueFrame
    bgrRangeFrame_GLower: AdjustValueFrame
    bgrRangeFrame_GUpper: AdjustValueFrame
    bgrRangeFrame_RLower: AdjustValueFrame
    bgrRangeFrame_RUpper: AdjustValueFrame
    bgr_min_range: InputParamFrame
    bgr_max_range: InputParamFrame
    btnShowBgrImage: VisionButton

    # BGR + HSV Range
    bgr_hsvRangeFrame: VisionFrame = None
    bgr_hsvRangeFrame_BLower: AdjustValueFrame
    bgr_hsvRangeFrame_BUpper: AdjustValueFrame
    bgr_hsvRangeFrame_GLower: AdjustValueFrame
    bgr_hsvRangeFrame_GUpper: AdjustValueFrame
    bgr_hsvRangeFrame_RLower: AdjustValueFrame
    bgr_hsvRangeFrame_RUpper: AdjustValueFrame
    bgr_hsvRangeFrame_HLower: AdjustValueFrame
    bgr_hsvRangeFrame_HUpper: AdjustValueFrame
    bgr_hsvRangeFrame_SLower: AdjustValueFrame
    bgr_hsvRangeFrame_SUpper: AdjustValueFrame
    bgr_hsvRangeFrame_VLower: AdjustValueFrame
    bgr_hsvRangeFrame_VUpper: AdjustValueFrame
    bgr_hsv_min_range: InputParamFrame
    bgr_hsv_max_range: InputParamFrame

    # BGR + HLS Range
    bgr_hlsRangeFrame: VisionFrame = None
    bgr_hlsRangeFrame_HLower: AdjustValueFrame
    bgr_hlsRangeFrame_HUpper: AdjustValueFrame
    bgr_hlsRangeFrame_LLower: AdjustValueFrame
    bgr_hlsRangeFrame_LUpper: AdjustValueFrame
    bgr_hlsRangeFrame_SLower: AdjustValueFrame
    bgr_hlsRangeFrame_SUpper: AdjustValueFrame
    bgr_hlsRangeFrame_BLower: AdjustValueFrame
    bgr_hlsRangeFrame_BUpper: AdjustValueFrame
    bgr_hlsRangeFrame_GLower: AdjustValueFrame
    bgr_hlsRangeFrame_GUpper: AdjustValueFrame
    bgr_hlsRangeFrame_RLower: AdjustValueFrame
    bgr_hlsRangeFrame_RUpper: AdjustValueFrame
    bgr_hls_min_range: InputParamFrame
    bgr_hls_max_range: InputParamFrame

    # Focus checking
    focusCheckingFrame: VisionFrame = None
    focusThresh: InputParamFrame

    # Hough lines
    houghLinesFrame: VisionFrame = None
    hl_rho: InputParamFrame
    hl_theta: InputParamFrame
    hl_threshold: InputParamFrame
    hl_srn: InputParamFrame
    hl_stn: InputParamFrame
    hl_min_theta: InputParamFrame
    hl_max_theta: InputParamFrame
    hl_min_length: InputParamFrame
    hl_max_gap: InputParamFrame

    # Background subtraction
    bsFrame: VisionFrame = None
    bs_historyNum: InputParamFrame
    bs_dist2Threshold: InputParamFrame
    bs_detectShadows: CheckboxStepParamFrame
    bs_processImageIndex: SourceIdxCombo

    # translation move image:
    translationMoveFrame: VisionFrame = None
    trans_move_x: InputParamFrame
    trans_move_y: InputParamFrame

    # Reference Translation
    refereneceTranslationFrame: VisionFrame = None
    rt_referenceType: ComboForFixValue
    rt_destSourceIndex: SourceInput
    rt_baseSourceIndex: SourceInput

    # Draw circle
    drawCircleFrame: VisionFrame = None
    dc_centerX: InputParamFrame
    dc_centerY: InputParamFrame
    dc_radius: InputParamFrame
    dc_thickness: InputParamFrame
    dc_inputCircle: SourceInput

    # Get extreme
    typeExtreme: ComboForFixValue
    extremeFrame: VisionFrame = None
    ge_contourInput: SourceInput

    # Paint
    paintFrame: VisionFrame = None
    paintColorLbl: VisionLabel
    paintBlue: AdjustValueFrame
    paintGreen: AdjustValueFrame
    paintRed: AdjustValueFrame

    # Min area rectangle
    minAreaRectFrame: VisionFrame = None
    mar_source_contour: SourceInput

    # Barcode reader
    barcodeReaderFrame: VisionFrame = None
    # data matrix code reader 2
    dataMatrixReaderFrame: VisionFrame = None
    get_min_area_box: SourceInput

    # Find chess board corners
    findChessBoardCornersFrame: VisionFrame = None
    cbc_sizeX: InputParamFrame
    cbc_sizeY: InputParamFrame

    # Resize
    resizeFrame: VisionFrame = None
    rs_sizeX: InputParamFrame
    rs_sizeY: InputParamFrame
    rs_ratio: CheckboxStepParamFrame
    rs_fX: InputParamFrame
    rs_fY: InputParamFrame

    # connection Contours
    connectionContourFrame: VisionFrame = None
    cc_size: InputParamFrame
    cc_distance: InputParamFrame
    cc_location: InputParamFrame

    # Split channel
    splitChannelFrame: VisionFrame = None
    sc_channel_id: InputParamFrame

    # ocr tesseract
    ocr_tesseract_frame: VisionFrame = None
    available_language: ComboForFlexibleValue

    # Change color
    change_color_frame: VisionFrame = None
    change_color_code: ComboForFlexibleValue
    change_color_mask: SourceInput

    # Threshold average
    threshold_average_frame: VisionFrame = None
    ta_brightness_reflection: InputParamFrame

    # Distance measurement
    distance_P2P_frame: VisionFrame = None
    p2p_point1_source: SourceInput
    p2p_point2_source: SourceInput
    p2p_range: Range_Input

    distance_P2L_frame: VisionFrame = None
    p2l_point_source: SourceInput
    p2l_point1_line_source: SourceInput
    p2l_point2_line_source: SourceInput
    p2l_range: Range_Input

    angle_from_2_lines_frame: VisionFrame = None
    af2l_point1_line1: SourceInput
    af2l_point2_line1: SourceInput
    af2l_point1_line2: SourceInput
    af2l_point2_line2: SourceInput
    af2l_valid_range: Range_Input

    # DDK scratch DL
    ddk_scratch_dl_frame: VisionFrame = None
    dl_thresh: InputParamFrame
    dl_resizeWidth: InputParamFrame
    dl_resizeHeight: InputParamFrame

    # Ignore area
    ignore_area_frame: VisionFrame = None
    ignore_areas: [IgnoreArea] = []
    btn_show_all_ignore_areas: VisionButton = None
    btn_delete_all_ignore_areas: VisionButton = None

    # select area
    multi_select_area_fr: VisionFrame = None
    select_area_list: [IgnoreArea] = []
    btn_show_all_select_areas: VisionButton = None
    btn_delete_all_select_areas: VisionButton = None

    rotateImageWithAngleFrame: VisionFrame = None
    riwa_angle: InputParamFrame
    riwa_reshape: CheckboxStepParamFrame

    brightness_change_frame: VisionFrame = None
    bright_change_type: ComboForFlexibleValue
    brightness_change_value: Slider_Input_Frame

    histogramEqualizationFrame: VisionFrame = None
    his_equ_type: ComboForFlexibleValue
    his_equ_clip_limit: Slider_Input_Frame
    his_equ_grid_size: Slider_Input_Frame

    gama_correction_frame: VisionFrame = None
    gama_corrention_value: Slider_Input_Frame
    measuransCvtFrame: VisionFrame = None

    referenceEdgeCornerFrame: VisionFrame = None
    rec_type: ComboForFixValue
    rec_thresh_type: ComboForFixValue
    rec_thresh: InputParamFrame
    rec_area: InputParamFrame
    rec_btn_get_reference_btn: VisionButton

    # Flood fill
    floodFillFrame: VisionFrame = None
    flood_fill_color: InputParamFrame
    flood_fill_seed_point: Coordinate_Input
    flood_fill_lowdiff: Slider_Input_Frame
    flood_fill_updiff: Slider_Input_Frame

    # Viet OCR
    viet_ocr_frame: VisionFrame = None
    vo_model: ComboForFlexibleValue
    vo_weight_file: Select_Path_File
    vo_device: ComboForFlexibleValue
    vo_vocab_file: Select_Path_File

    # Contour linear regression
    contour_linear_regression_frame: VisionFrame = None
    clr_contour_source: SourceInput
    clr_area_source: SourceInput

    # Contours Approximation
    contour_apprx_frame: VisionFrame  = None
    c_apprx_source_contour: SourceInput
    c_apprx_epsilon_percent: Slider_Input_Frame
    c_apprx_closed: CheckboxStepParamFrame

    # Contours fit line
    contours_fit_line_frame: VisionFrame = None
    cfl_source_contour: SourceInput
    cfl_distance_type: ComboForFixValue
    cfl_param: InputParamFrame
    cfl_reps: Slider_Input_Frame
    cfl_aeps: Slider_Input_Frame

    """yolo v8"""
    segmentation_yolov8_frame: VisionFrame = None
    path_weight_yolov8: Select_Path_File = None
    confidence_yolov8: InputParamFrame = None
    load_model_yolov8: VisionButton = None

    """multi select area 2"""
    auto_multi_circle_fr: VisionFrame = None
    amc_circle_list: SourceInput
    amc_radius_1: InputParamFrame
    amc_radius_2: InputParamFrame

    yDistance = 30
    xDistance = 150

    def __init__(self, master, mainWindow):
        from View.Researching.ResearchingTab import ResearchingTab
        from MainWindow import MainWindow

        VisionLabelFrame.__init__(self, master=master)
        self.mainWindow: MainWindow = mainWindow
        self.masterWin: ResearchingTab = master
        self.initBaseValue()
        self.setupView()
        self.setupButton()

    def initBaseValue(self):
        self.stepList = []
        self.stepList.append("Reference Image")
        self.stepList.append("Template")
        self.stepList.append("None")
        self.stepList.append("Original Image")
        for i in range(self.mainWindow.algorithmManager.maxStep):
            self.stepList.append("Step {}".format(i))

    def setupView(self):
        self.setupParameterFrame()

    def updateParameter(self, stepParameter):
        self.stepParameter = stepParameter

        if self.currentFrame is not None:
            self.currentFrame.place_forget()

        # Hough circle or Average hough circles
        if stepParameter.stepAlgorithmName == MethodList.houghCircle.value \
                or stepParameter.stepAlgorithmName == MethodList.averageHoughCircle.value:
            if self.houghCircleSettingFrame is None:
                self.setupHoughCircleFrame()
            self.currentFrame = self.houghCircleSettingFrame
            self.maxRadiusHoughCircle.setValue(self.stepParameter.houghCircleMaxRadius)
            self.parm1HoughCircle.setValue(self.stepParameter.houghCircleParm1)
            self.parm2HoughCircle.setValue(self.stepParameter.houghCircleParm2)
            self.minRadiusHoughCircle.setValue(self.stepParameter.houghCircleMinRadius)
            self.minDistHoughCircle.setValue(self.stepParameter.houghCircleMinDist)
            self.betweenDistHoughCircle.setValue(self.stepParameter.houghCircleBetweenDist)
            self.trustNumberHoughCircle.setValue(self.stepParameter.houghCircleTrustNumber)

        # threshold
        elif stepParameter.stepAlgorithmName == MethodList.threshold.value:
            if self.thresholdFrame is None:
                self.setupThresholdFrame()
            self.currentFrame = self.thresholdFrame
            self.threshold_thresh_val.setValue(self.stepParameter.threshold_thresh_val)
            self.maxThresValueEntry.setValue(self.stepParameter.maxThresholdValue)
            self.threshType1Combo.setStringValue(self.stepParameter.thresholdType1)
            self.threshType2Combo.setStringValue(self.stepParameter.thresholdType2)

        # color detect
        elif stepParameter.stepAlgorithmName == MethodList.colorDetect.value:
            if self.colorDetectFrame is None:
                self.setupColorDetectFrame()
            self.currentFrame = self.colorDetectFrame

            self.bCDToleranceEntry.delete(0, END)
            self.bCDToleranceEntry.insert(0, "{}".format(self.stepParameter.bgrToleranceRange[0]))

            self.gCDToleranceEntry.delete(0, END)
            self.gCDToleranceEntry.insert(0, "{}".format(self.stepParameter.bgrToleranceRange[1]))

            self.rCDToleranceEntry.delete(0, END)
            self.rCDToleranceEntry.insert(0, "{}".format(self.stepParameter.bgrToleranceRange[2]))

            self.countNonZeroThreshCD.setValue(self.stepParameter.nonzeroThresh)

            self.showBaseColor()

        # In range
        elif stepParameter.stepAlgorithmName == MethodList.inRange.value:
            if self.inRangeFrame is None:
                self.setupInRangeFrame()
            self.currentFrame = self.inRangeFrame

            self.bIRToleranceEntry.delete(0, END)
            self.bIRToleranceEntry.insert(0, "{}".format(self.stepParameter.bgrToleranceRange[0]))

            self.gIRToleranceEntry.delete(0, END)
            self.gIRToleranceEntry.insert(0, "{}".format(self.stepParameter.bgrToleranceRange[1]))

            self.rIRToleranceEntry.delete(0, END)
            self.rIRToleranceEntry.insert(0, "{}".format(self.stepParameter.bgrToleranceRange[2]))

            self.showBaseColor()

        # Count nonzero
        elif stepParameter.stepAlgorithmName == MethodList.countNonzero.value:
            if self.countNonzeroFame is None:
                self.setupCountNonzeroFrame()
            self.currentFrame = self.countNonzeroFame
            # self.countNonZeroThresh.setValue(self.stepParameter.nonzeroThresh)
            self.nonzero_min_range.setValue(self.stepParameter.minRange)
            self.nonzero_max_range.setValue(self.stepParameter.maxRange)

        # Convert Color
        elif stepParameter.stepAlgorithmName == MethodList.cvtColor.value:
            if self.cvtColorFrame is None:
                self.setupCvtColorFrame()
            self.currentFrame = self.cvtColorFrame
            self.cvtColorCode.setStringValue(self.stepParameter.cvtColorCode)

        # Blur
        elif stepParameter.stepAlgorithmName == MethodList.medianBlur.value or \
                stepParameter.stepAlgorithmName == MethodList.gaussianBlur.value or \
                stepParameter.stepAlgorithmName == MethodList.blur.value:
            if self.medianBlurFrame is None:
                self.setupMedianBlurFrame()
            self.currentFrame = self.medianBlurFrame
            self.blurSize.setValue(self.stepParameter.blurSize)
            self.blurSigmaX.setValue(self.stepParameter.blurSigmaX)
        # Rotate image with angle
        elif stepParameter.stepAlgorithmName == MethodList.rotate_with_angle.value:
            if self.rotateImageWithAngleFrame is None:
                self.setupRotateImageWithAngleFrame()
            self.currentFrame = self.rotateImageWithAngleFrame
            self.riwa_angle.setValue(self.stepParameter.riwa_angle)
            self.riwa_reshape.setValue(self.stepParameter.riwa_reshape)

        # Matching template
        elif stepParameter.stepAlgorithmName == MethodList.matchingTemplate.value:
            if self.matchingTemplateFrame is None:
                self.setupMatchingTemplateFrame()
            self.currentFrame = self.matchingTemplateFrame
            self.minMatchingValue.setValue(self.stepParameter.minMatchingValue)
            self.multiMatching.setValue(self.stepParameter.multiMatchingFlag)
        # Find contours
        elif self.stepParameter.stepAlgorithmName == MethodList.findContour.value \
                or self.stepParameter.stepAlgorithmName == MethodList.fillContour.value \
                or self.stepParameter.stepAlgorithmName == MethodList.getImageInsideContour.value \
                or self.stepParameter.stepAlgorithmName == MethodList.countContour.value:
            if self.findContoursFrame is None:
                self.setupFindContoursFrame()
            self.currentFrame = self.findContoursFrame
            self.contours_binarySource.setValue(self.stepParameter.contours_binary_source)
            self.contours_areaSource.setValue(self.stepParameter.contours_area_source)
            self.minContoursArea.setValue(self.stepParameter.minAreaContours)
            self.maxContoursArea.setValue(self.stepParameter.maxAreaContours)
            self.minContoursWidth.setValue(self.stepParameter.minWidthContours)
            self.maxContoursWidth.setValue(self.stepParameter.maxWidthContours)
            self.minContoursHeight.setValue(self.stepParameter.minHeightContours)
            self.maxContoursHeight.setValue(self.stepParameter.maxHeightContours)
            self.minAspectRatio.setValue(self.stepParameter.minAspectRatio)
            self.maxAspectRatio.setValue(self.stepParameter.maxAspectRatio)
            self.numContourThresh.setValue(self.stepParameter.contourNumThresh)

        # Erode, Dilate
        elif stepParameter.stepAlgorithmName == MethodList.dilate.value or stepParameter.stepAlgorithmName == MethodList.erode.value:
            if self.dilateFrame is None:
                self.setupDilateAndErodeFrame()
            self.currentFrame = self.dilateFrame
            self.kernelSizeX.setValue(self.stepParameter.kernelSizeX)
            self.kernelSizeY.setValue(self.stepParameter.kernelSizeY)
            self.iterations.setValue(self.stepParameter.iterations)
        # Bit wise
        elif stepParameter.stepAlgorithmName == MethodList.bitwiseAnd.value \
                or stepParameter.stepAlgorithmName == MethodList.bitwiseOr.value \
                or stepParameter.stepAlgorithmName == MethodList.bitwiseNot.value \
                or stepParameter.stepAlgorithmName == MethodList.bitwiseXor.value:
            if self.bitwiseFrame is None:
                self.setupBitWiseFrame()
            self.currentFrame = self.bitwiseFrame
            self.sourceImage2.setPosValue(stepParameter.resource2Index + 4)
            self.maskImage.setPosValue(stepParameter.maskIndex + 4)
        # Adaptive thresh holding
        elif stepParameter.stepAlgorithmName == MethodList.adaptiveThreshold.value:
            if self.adaptiveThresholdFrame is None:
                self.setupAdaptiveThresholdFrame()
            self.currentFrame = self.adaptiveThresholdFrame
            self.adaptiveThreshMaxVal.setValue(stepParameter.maxThresholdValue)
            self.adaptiveMode.setStringValue(stepParameter.adaptiveMode)
            self.adaptiveThreshType.setStringValue(stepParameter.thresholdType1)
            self.adaptiveBlockSize.setValue(stepParameter.blockSize)
            self.adaptiveChangeVal.setValue(stepParameter.adaptiveC)
        # Canny
        elif stepParameter.stepAlgorithmName == MethodList.canny.value:
            if self.cannyFrame is None:
                self.setupCannyFrame()
            self.currentFrame = self.cannyFrame
            self.cannyMinThresh.setValue(stepParameter.minThresh)
            self.cannyMaxThresh.setValue(stepParameter.maxThresholdValue)
            self.canny_kernel_size.setValue(stepParameter.canny_kernel_size)
        # Rotate
        elif stepParameter.stepAlgorithmName == MethodList.rotate.value:
            if self.rotateFrame is None:
                self.setupRotateFrame()
            self.currentFrame = self.rotateFrame
            self.rotateCode.setStringValue(stepParameter.rotateCode)
            self.rt_angle.setValue(stepParameter.rt_angle)
            self.rt_centerX.setValue(stepParameter.rt_center[0])
            self.rt_centerY.setValue(stepParameter.rt_center[1])
        # Flip
        elif stepParameter.stepAlgorithmName == MethodList.flip.value:
            if self.flipFrame is None:
                self.setupFlipFrame()
            self.currentFrame = self.flipFrame
            self.flipCode.setStringValue(stepParameter.flipCode)
        # Original reference image
        elif stepParameter.stepAlgorithmName == MethodList.originalReference.value:
            if self.originalReferenceFrame is None:
                self.setupOriginalReferenceFrame()
            self.currentFrame = self.originalReferenceFrame
            self.orRef1StepIdx.setPosValue(stepParameter.orRef1StepIdx)
            self.orRef2StepIdx.setPosValue(stepParameter.orRef2StepIdx)
            self.orRef3StepIdx.setPosValue(stepParameter.orRef3StepIdx)
        # Hls range
        elif stepParameter.stepAlgorithmName == MethodList.hlsInRange.value:
            if self.hlsRangeFrame is None:
                self.setupHLSRangeFrame()
            self.currentFrame = self.hlsRangeFrame
            self.hlsRangeFrame_HLower.setValue(stepParameter.hlsLower[0])
            self.hlsRangeFrame_LLower.setValue(stepParameter.hlsLower[1])
            self.hlsRangeFrame_SLower.setValue(stepParameter.hlsLower[2])

            self.hlsRangeFrame_HUpper.setValue(stepParameter.hlsUpper[0])
            self.hlsRangeFrame_LUpper.setValue(stepParameter.hlsUpper[1])
            self.hlsRangeFrame_SUpper.setValue(stepParameter.hlsUpper[2])

            self.hls_min_range.setValue(stepParameter.minRange)
            self.hls_max_range.setValue(stepParameter.maxRange)

        # Hsv Range
        elif stepParameter.stepAlgorithmName == MethodList.hsvInRange.value:
            if self.hsvRangeFrame is None:
                self.setupHSVRangeFrame()
            self.currentFrame = self.hsvRangeFrame
            self.hsvRangeFrame_HLower.setValue(stepParameter.hsvLower[0])
            self.hsvRangeFrame_SLower.setValue(stepParameter.hsvLower[1])
            self.hsvRangeFrame_VLower.setValue(stepParameter.hsvLower[2])

            self.hsvRangeFrame_HUpper.setValue(stepParameter.hsvUpper[0])
            self.hsvRangeFrame_SUpper.setValue(stepParameter.hsvUpper[1])
            self.hsvRangeFrame_VUpper.setValue(stepParameter.hsvUpper[2])

            self.hsv_min_range.setValue(stepParameter.minRange)
            self.hsv_max_range.setValue(stepParameter.maxRange)
        # HSV + HLS range
        elif stepParameter.stepAlgorithmName == MethodList.hsv_hlsRange.value:
            if self.hsv_hlsRangeFrame is None:
                self.setupHSV_HLSRangeFrame()
            self.currentFrame = self.hsv_hlsRangeFrame
            self.hsv_hlsRangeFrame_VHLower.setValue(stepParameter.hsvLower[0])
            self.hsv_hlsRangeFrame_VSLower.setValue(stepParameter.hsvLower[1])
            self.hsv_hlsRangeFrame_VVLower.setValue(stepParameter.hsvLower[2])

            self.hsv_hlsRangeFrame_VHUpper.setValue(stepParameter.hsvUpper[0])
            self.hsv_hlsRangeFrame_VSUpper.setValue(stepParameter.hsvUpper[1])
            self.hsv_hlsRangeFrame_VVUpper.setValue(stepParameter.hsvUpper[2])

            self.hsv_hlsRangeFrame_SHLower.setValue(stepParameter.hlsLower[0])
            self.hsv_hlsRangeFrame_SLLower.setValue(stepParameter.hlsLower[1])
            self.hsv_hlsRangeFrame_SSLower.setValue(stepParameter.hlsLower[2])

            self.hsv_hlsRangeFrame_SHUpper.setValue(stepParameter.hlsUpper[0])
            self.hsv_hlsRangeFrame_SLUpper.setValue(stepParameter.hlsUpper[1])
            self.hsv_hlsRangeFrame_SSUpper.setValue(stepParameter.hlsUpper[2])

            self.hsv_hls_min_range.setValue(stepParameter.minRange)
            self.hsv_hls_max_range.setValue(stepParameter.maxRange)

        # BGR range
        elif stepParameter.stepAlgorithmName == MethodList.bgrInRange.value:
            if self.bgrRangeFrame is None:
                self.setupBGRRangeFrame()
            self.currentFrame = self.bgrRangeFrame
            self.bgrRangeFrame_BLower.setValue(stepParameter.bgrLower[0])
            self.bgrRangeFrame_GLower.setValue(stepParameter.bgrLower[1])
            self.bgrRangeFrame_RLower.setValue(stepParameter.bgrLower[2])

            self.bgrRangeFrame_BUpper.setValue(stepParameter.bgrUpper[0])
            self.bgrRangeFrame_GUpper.setValue(stepParameter.bgrUpper[1])
            self.bgrRangeFrame_RUpper.setValue(stepParameter.bgrUpper[2])

            self.bgr_min_range.setValue(stepParameter.minRange)
            self.bgr_max_range.setValue(stepParameter.maxRange)
        # BGR + HLS range
        elif stepParameter.stepAlgorithmName == MethodList.bgr_hlsRange.value:
            if self.bgr_hlsRangeFrame is None:
                self.setupBGR_HLSRangeFrame()
            self.currentFrame = self.bgr_hlsRangeFrame
            self.bgr_hlsRangeFrame_BLower.setValue(stepParameter.bgrLower[0])
            self.bgr_hlsRangeFrame_GLower.setValue(stepParameter.bgrLower[1])
            self.bgr_hlsRangeFrame_RLower.setValue(stepParameter.bgrLower[2])

            self.bgr_hlsRangeFrame_BUpper.setValue(stepParameter.bgrUpper[0])
            self.bgr_hlsRangeFrame_GUpper.setValue(stepParameter.bgrUpper[1])
            self.bgr_hlsRangeFrame_RUpper.setValue(stepParameter.bgrUpper[2])

            self.bgr_hlsRangeFrame_HLower.setValue(stepParameter.hlsLower[0])
            self.bgr_hlsRangeFrame_LLower.setValue(stepParameter.hlsLower[1])
            self.bgr_hlsRangeFrame_SLower.setValue(stepParameter.hlsLower[2])

            self.bgr_hlsRangeFrame_HUpper.setValue(stepParameter.hlsUpper[0])
            self.bgr_hlsRangeFrame_LUpper.setValue(stepParameter.hlsUpper[1])
            self.bgr_hlsRangeFrame_SUpper.setValue(stepParameter.hlsUpper[2])

            self.bgr_hls_min_range.setValue(stepParameter.minRange)
            self.bgr_hls_max_range.setValue(stepParameter.maxRange)
        # BGR + HSV range
        elif stepParameter.stepAlgorithmName == MethodList.bgr_hsvRange.value:
            if self.bgr_hsvRangeFrame is None:
                self.setupBGR_HSVRangeFrame()
            self.currentFrame = self.bgr_hsvRangeFrame
            self.bgr_hsvRangeFrame_BLower.setValue(stepParameter.bgrLower[0])
            self.bgr_hsvRangeFrame_GLower.setValue(stepParameter.bgrLower[1])
            self.bgr_hsvRangeFrame_RLower.setValue(stepParameter.bgrLower[2])

            self.bgr_hsvRangeFrame_BUpper.setValue(stepParameter.bgrUpper[0])
            self.bgr_hsvRangeFrame_GUpper.setValue(stepParameter.bgrUpper[1])
            self.bgr_hsvRangeFrame_RUpper.setValue(stepParameter.bgrUpper[2])

            self.bgr_hsvRangeFrame_HLower.setValue(stepParameter.hsvLower[0])
            self.bgr_hsvRangeFrame_SLower.setValue(stepParameter.hsvLower[1])
            self.bgr_hsvRangeFrame_VLower.setValue(stepParameter.hsvLower[2])

            self.bgr_hsvRangeFrame_HUpper.setValue(stepParameter.hsvUpper[0])
            self.bgr_hsvRangeFrame_SUpper.setValue(stepParameter.hsvUpper[1])
            self.bgr_hsvRangeFrame_VUpper.setValue(stepParameter.hsvUpper[2])

            self.bgr_hsv_min_range.setValue(stepParameter.minRange)
            self.bgr_hsv_max_range.setValue(stepParameter.maxRange)
        # Focus checking
        elif stepParameter.stepAlgorithmName == MethodList.focusChecking.value:
            if self.focusCheckingFrame is None:
                self.setupFocusCheckingFrame()
            self.currentFrame = self.focusCheckingFrame
            self.focusThresh.setValue(stepParameter.threshFocus)
        # Hough lines
        elif stepParameter.stepAlgorithmName == MethodList.houghLines.value or \
                self.stepParameter.stepAlgorithmName == MethodList.houghLinesP.value:
            if self.houghLinesFrame is None:
                self.setupHoughLinesFrame()
            self.currentFrame = self.houghLinesFrame
            self.hl_rho.setValue(stepParameter.hl_rho)
            self.hl_theta.setValue(stepParameter.hl_theta)
            self.hl_threshold.setValue(stepParameter.hl_threshold)
            self.hl_min_theta.setValue(stepParameter.hl_min_theta)
            self.hl_max_theta.setValue(stepParameter.hl_max_theta)
            self.hl_srn.setValue(stepParameter.hl_srn)
            self.hl_stn.setValue(stepParameter.hl_stn)
            self.hl_min_length.setValue(stepParameter.hl_min_length)
            self.hl_max_gap.setValue(stepParameter.hl_max_gap)
        # background subtraction
        elif stepParameter.stepAlgorithmName == MethodList.subtractionMog2.value or \
                stepParameter.stepAlgorithmName == MethodList.subtractionKNN.value:
            if self.bsFrame is None:
                self.setupBSFrame()
            self.currentFrame = self.bsFrame
            self.bs_historyNum.setValue(stepParameter.bs_history_frame_num)
            self.bs_dist2Threshold.setValue(stepParameter.bs_dist2Threshold)
            self.bs_detectShadows.setValue(stepParameter.bs_detect_shadow)
            self.bs_processImageIndex.setPosValue(stepParameter.bs_process_image_index + 4)
        # translation
        elif stepParameter.stepAlgorithmName == MethodList.translation.value:
            if self.translationMoveFrame is None:
                self.setupTranslationMoveFrame()
            self.currentFrame = self.translationMoveFrame
            self.trans_move_x.setValue(stepParameter.trans_move_x)
            self.trans_move_y.setValue(stepParameter.trans_move_y)
        # reference translation
        elif stepParameter.stepAlgorithmName == MethodList.referenceTranslation.value:
            if self.refereneceTranslationFrame is None:
                self.setupReferenceTranslation()
            self.currentFrame = self.refereneceTranslationFrame
            self.rt_baseSourceIndex.setValue(stepParameter.rt_baseSource)
            self.rt_destSourceIndex.setValue(stepParameter.rt_destSource)
            self.rt_referenceType.setStringValue(stepParameter.rt_type)
        # Draw circle
        elif stepParameter.stepAlgorithmName == MethodList.drawCircle.value:
            if self.drawCircleFrame is None:
                self.setupDrawCircleFrame()
            self.currentFrame = self.drawCircleFrame
            self.dc_centerX.setValue(stepParameter.dc_center[0])
            self.dc_centerY.setValue(stepParameter.dc_center[1])
            self.dc_radius.setValue(stepParameter.dc_radius)
            self.dc_thickness.setValue(stepParameter.dc_thickness)
            self.dc_inputCircle.setValue(stepParameter.dc_circleInput)
        # Get extreme
        elif stepParameter.stepAlgorithmName == MethodList.getExtreme.value:
            if self.extremeFrame is None:
                self.setupExtremeFrame()
            self.currentFrame = self.extremeFrame
            self.typeExtreme.setStringValue(stepParameter.ge_extremeType)
            self.ge_contourInput.setValue(stepParameter.ge_sourceContour)

        # Paint
        elif stepParameter.stepAlgorithmName == MethodList.paint.value:
            if self.paintFrame is None:
                self.setupPaintFrame()
            self.currentFrame = self.paintFrame
            self.paintBlue.setValue(stepParameter.paintColor[0])
            self.paintGreen.setValue(stepParameter.paintColor[1])
            self.paintRed.setValue(stepParameter.paintColor[2])
        # Min area rectangle
        elif stepParameter.stepAlgorithmName == MethodList.getMinAreaRect.value:
            if self.minAreaRectFrame is None:
                self.setupMinAreaRectFrame()
            self.currentFrame = self.minAreaRectFrame
            self.mar_source_contour.setValue(stepParameter.mar_source_contours)

        # Barcode reader
        elif stepParameter.stepAlgorithmName == MethodList.barcodeReader.value or \
                stepParameter.stepAlgorithmName == MethodList.dataMatrixReader.value:
            if self.barcodeReaderFrame is None:
                self.setupBarcodeReaderFrame()
            self.currentFrame = self.barcodeReaderFrame

        # DATA matrix reader with get min area
        elif stepParameter.stepAlgorithmName == MethodList.dataMatrixReaderWithArea.value:
            if self.dataMatrixReaderFrame is None:
                self.setupDataMatrix2ReaderFrame()
            self.currentFrame = self.dataMatrixReaderFrame
            self.get_min_area_box.setValue(stepParameter.get_min_area_box)

        # Find chessboard Corners
        elif stepParameter.stepAlgorithmName == MethodList.findChessBoardCorners.value:
            if self.findChessBoardCornersFrame is None:
                self.setupFindChessBoardCornersFrame()
            self.currentFrame = self.findChessBoardCornersFrame
            self.cbc_sizeX.setValue(self.stepParameter.cbc_sizeX)
            self.cbc_sizeY.setValue(stepParameter.cbc_sizeY)
        # Resize
        elif stepParameter.stepAlgorithmName == MethodList.resize.value:
            if self.resizeFrame is None:
                self.setupResizeFrame()
            self.currentFrame = self.resizeFrame
            self.rs_sizeX.setValue(stepParameter.rs_sizeX)
            self.rs_sizeY.setValue(stepParameter.rs_sizeY)
            self.rs_ratio.setValue(stepParameter.rs_ratio)
            self.rs_fX.setValue(stepParameter.rs_fX)
            self.rs_fY.setValue(stepParameter.rs_fY)

        # Connection contours
        elif stepParameter.stepAlgorithmName == MethodList.connectionContour.value:
            if self.connectionContourFrame is None:
                self.setupConnectionContourFrame()
            self.currentFrame = self.connectionContourFrame
            self.cc_size.setValue(stepParameter.cc_size)
            self.cc_distance.setValue(stepParameter.cc_distance)
            self.cc_location.setValue(stepParameter.cc_location)

        # Split channel
        elif stepParameter.stepAlgorithmName == MethodList.splitChannel.value:
            if self.splitChannelFrame is None:
                self.setupSplitChannelFrame()
            self.currentFrame = self.splitChannelFrame
            self.sc_channel_id.setValue(stepParameter.sc_channel_id)
        # tesseract
        elif stepParameter.stepAlgorithmName == MethodList.ocr_tesseract.value:
            if self.ocr_tesseract_frame is None:
                self.setup_ocr_tesseract_Frame()
            self.currentFrame = self.ocr_tesseract_frame
            self.available_language.setStringValue(stepParameter.ocr_tes_lange)

        # Change color
        elif stepParameter.stepAlgorithmName == MethodList.changeColor.value:
            if self.change_color_frame is None:
                self.setup_change_color_frame()
            self.currentFrame = self.change_color_frame
            self.change_color_code.setStringValue(stepParameter.change_color_code)
            self.change_color_mask.setValue(stepParameter.change_color_mask)

        # Threshold average
        elif stepParameter.stepAlgorithmName == MethodList.threshold_average.value:
            if self.threshold_average_frame is None:
                self.setup_threshold_average_frame()
            self.currentFrame = self.threshold_average_frame
            self.ta_brightness_reflection.setValue(stepParameter.ta_brightness_reflection)

        # Distance measurement
        elif stepParameter.stepAlgorithmName == MethodList.distance_point_to_point.value:
            if self.distance_P2P_frame is None:
                self.setup_distance_point_to_point_frame()
            self.currentFrame = self.distance_P2P_frame
            self.p2p_point1_source.setValue(stepParameter.p2p_point1)
            self.p2p_point2_source.setValue(stepParameter.p2p_point2)
            self.p2p_range.setValue(stepParameter.p2p_range)

        elif stepParameter.stepAlgorithmName == MethodList.distance_point_to_line.value:
            if self.distance_P2L_frame is None:
                self.setup_distance_point_to_line_frame()
            self.currentFrame = self.distance_P2L_frame
            self.p2l_point_source.setValue(stepParameter.p2l_point)
            self.p2l_point1_line_source.setValue(stepParameter.p2l_point1_line)
            self.p2l_point2_line_source.setValue(stepParameter.p2l_point2_line)
            self.p2l_range.setValue(stepParameter.p2l_range)

        # Angle measurement
        elif stepParameter.stepAlgorithmName == MethodList.angle_from_2_lines.value:
            if self.angle_from_2_lines_frame is None:
                self.setup_angle_from_2_lines()
            self.currentFrame = self.angle_from_2_lines_frame
            self.af2l_point1_line1.setValue(stepParameter.af2l_point1_line1)
            self.af2l_point2_line1.setValue(stepParameter.af2l_point2_line1)
            self.af2l_point1_line2.setValue(stepParameter.af2l_point1_line2)
            self.af2l_point2_line2.setValue(stepParameter.af2l_point2_line2)
            self.af2l_valid_range.setValue(stepParameter.af2l_valid_range)

        # Deep learning for DDK
        elif stepParameter.stepAlgorithmName == MethodList.ddk_scratch_dl.value:
            if self.ddk_scratch_dl_frame is None:
                self.setup_ddk_scratch_dl_frame()
            self.currentFrame = self.ddk_scratch_dl_frame
            self.dl_thresh.setValue(stepParameter.dl_thresh)
            self.dl_resizeWidth.setValue(stepParameter.dl_resize_shape[0])
            self.dl_resizeHeight.setValue(stepParameter.dl_resize_shape[1])
        # Ignore areas
        elif stepParameter.stepAlgorithmName == MethodList.ignore_areas.value:
            if self.ignore_area_frame is None:
                self.setup_ignore_area_frame()
            self.currentFrame = self.ignore_area_frame
            self.update_ignore_area_list(self.stepParameter.ignore_areas_list)

        # Multi select area
        elif stepParameter.stepAlgorithmName == MethodList.multi_select_area.value:
            if self.multi_select_area_fr is None:
                self.setup_multi_select_area()
            self.currentFrame = self.multi_select_area_fr
            self.update_multi_select_area_list(self.stepParameter.select_areas_list)


        # Change brightness
        elif stepParameter.stepAlgorithmName == MethodList.brightness_change.value:
            if self.brightness_change_frame is None:
                self.setupBrightnessChangeFrame()
            self.currentFrame = self.brightness_change_frame
            self.bright_change_type.setStringValue(self.stepParameter.change_brightness_type)
            self.brightness_change_value.setValue(self.stepParameter.change_brightness_value)
        # Histogram Equalization
        elif stepParameter.stepAlgorithmName == MethodList.histogram_equalization.value:
            if self.histogramEqualizationFrame is None:
                self.setupHistogramEqualizationFrame()
            self.currentFrame = self.histogramEqualizationFrame
            self.his_equ_type.setStringValue(self.stepParameter.he_type)
            self.his_equ_clip_limit.setValue(self.stepParameter.he_clipLimit)
            self.his_equ_grid_size.setValue(self.stepParameter.he_tile_grid_size)

        # Gama correction
        elif stepParameter.stepAlgorithmName == MethodList.gama_correction.value:
            if self.gama_correction_frame is None:
                self.setup_gama_correction_frame()
            self.currentFrame = self.gama_correction_frame
            self.gama_corrention_value.setValue(self.stepParameter.gama_correction_value)
        # Reference Edge corner
        elif stepParameter.stepAlgorithmName == MethodList.reference_edge_corner.value:
            if self.referenceEdgeCornerFrame is None:
                self.setupReferenceEdgeCorner()
            self.currentFrame = self.referenceEdgeCornerFrame
            self.rec_thresh_type.setStringValue(stepParameter.rec_thresh_type)
            self.rec_type.setStringValue(stepParameter.rec_type)
            self.rec_thresh.setValue(stepParameter.rec_thresh)
            self.rec_area.setValue(stepParameter.rec_area)

        # Flood fill
        elif stepParameter.stepAlgorithmName == MethodList.floodFill.value:
            if self.floodFillFrame is None:
                self.setupFloodFillFrame()
            self.currentFrame = self.floodFillFrame
            self.flood_fill_seed_point.setValue(stepParameter.flood_fill_seed_point)
            self.flood_fill_color.setValue(stepParameter.flood_fill_color)
            self.flood_fill_lowdiff.setValue(stepParameter.flood_fill_lowdiff)
            self.flood_fill_updiff.setValue(stepParameter.flood_fill_updiff)
        elif stepParameter.stepAlgorithmName == MethodList.viet_ocr.value:
            if self.viet_ocr_frame is None:
                self.setup_viet_ocr_frame()
            self.currentFrame = self.viet_ocr_frame
            self.vo_model.setStringValue(stepParameter.vo_model)
            self.vo_weight_file.setValue(stepParameter.vo_weight_file_path)
            self.vo_device.setStringValue(stepParameter.vo_device)
            self.vo_vocab_file.setValue(stepParameter.vo_vocab_path_file)
        elif stepParameter.stepAlgorithmName == MethodList.contour_linear_regression.value:
            if self.contour_linear_regression_frame is None:
                self.setup_contour_linear_regression()
            self.currentFrame = self.contour_linear_regression_frame
            self.clr_contour_source.setValue(stepParameter.clr_source_contour)
            self.clr_area_source.setValue(stepParameter.clr_area_source)

        elif stepParameter.stepAlgorithmName == MethodList.contourApproximation.value:
            if self.contour_apprx_frame is None:
                self.setup_contours_approximation()
            self.currentFrame = self.contour_apprx_frame
            self.c_apprx_source_contour.setValue(stepParameter.c_apprx_source_contour)
            self.c_apprx_epsilon_percent.setValue(stepParameter.c_apprx_epsilon_percent)
            self.c_apprx_closed.setValue(stepParameter.c_apprx_closed)
        elif stepParameter.stepAlgorithmName == MethodList.fittingLine.value:
            if self.contours_fit_line_frame is None:
                self.setup_contours_fit_line()
            self.currentFrame = self.contours_fit_line_frame
            self.cfl_source_contour.setValue(stepParameter.cfl_source_contour)
            self.cfl_distance_type.setStringValue(stepParameter.cfl_distance_type)
            self.cfl_param.setValue(stepParameter.cfl_param)
            self.cfl_reps.setValue(stepParameter.cfl_reps)
            self.cfl_aeps.setValue(stepParameter.cfl_aeps)

        # Segmentation YoloV8
        elif stepParameter.stepAlgorithmName == MethodList.segment_yolov8.value:
            if self.segmentation_yolov8_frame is None:
                self.setup_yolov8()
            self.currentFrame = self.segmentation_yolov8_frame
            self.path_weight_yolov8.setValue(stepParameter.path_weight_yolov8)
            self.confidence_yolov8.setValue(stepParameter.confidence_yolov8)
            # Auto multi circle
        elif stepParameter.stepAlgorithmName == MethodList.auto_multi_circle.value:
            if self.auto_multi_circle_fr is None:
                self.setup_auto_multi_circle()
            self.currentFrame = self.auto_multi_circle_fr
            self.amc_circle_list.setValue(stepParameter.amc_circle_list)
            self.amc_radius_1.setValue(stepParameter.amc_circle_radius_1)
            self.amc_radius_2.setValue(stepParameter.amc_circle_radius_2)
        else:
            self.currentFrame = None

        if self.currentFrame is not None:
            self.currentFrame.place(x=0, y=35, relwidth=1, relheight=0.72)
        self.config(text=self.mainWindow.languageManager.localized("settingForStep").format(self.stepParameter.stepId,
                                                                                            self.stepParameter.stepAlgorithmName))
        # self.sourceImageCombobox.current(self.stepParameter.resourceIndex + 4)
        self.resourceImageIndex.setValue(stepParameter.resourceIndex)

    """
        segmentation yolo v8    
    """
    def setup_yolov8(self):
        self.segmentation_yolov8_frame = VisionFrame(self)

        self.path_weight_yolov8 = Select_Path_File(self.segmentation_yolov8_frame, "Weight file:",
                                                   yPos=0 * self.yDistance + 5, height=self.yDistance)
        self.load_model_yolov8 = VisionButton(self.segmentation_yolov8_frame, text="Load model",
                                                      command=self.click_btn_load_model)
        self.load_model_yolov8.place(x=5, y=1 * self.yDistance + 5, height=30)
        self.confidence_yolov8 = InputParamFrame(self.segmentation_yolov8_frame, "Confidence 0.0~1.0: ",
                                                 yPos=2 * self.yDistance + 5, height=self.yDistance)

    def click_btn_load_model(self):
        self.mainWindow.researchingTab.currentAlgorithm.load_model_yolo(path_model=self.path_weight_yolov8.getValue())
    """
        multi select area 2
    """
    def setup_auto_multi_circle(self):
        self.auto_multi_circle_fr = VisionFrame(self)
        self.amc_circle_list = SourceInput(self.auto_multi_circle_fr, "Tam tron",
                                           yPos=0 * self.yDistance + 5, height=self.yDistance,
                                           maxStep=self.mainWindow.algorithmManager.maxStep)
        self.amc_radius_1 = InputParamFrame(self.auto_multi_circle_fr, "Ban kinh 1", yPos=1 * self.yDistance + 5,
                                            height=self.yDistance)
        self.amc_radius_2 = InputParamFrame(self.auto_multi_circle_fr, "Ban kinh 2", yPos=2 * self.yDistance + 5,
                                            height=self.yDistance)

    def setup_contours_fit_line(self):
        self.contours_fit_line_frame = VisionFrame(self)
        self.cfl_source_contour = SourceInput(self.contours_fit_line_frame, "Source contours",
                                                  yPos=0 * self.yDistance + 5, height=self.yDistance,
                                                  maxStep=self.mainWindow.algorithmManager.maxStep)
        self.cfl_distance_type = ComboForFixValue(self.contours_fit_line_frame, "Distance type:",
                                                  yPos=1 * self.yDistance + 5, height=self.yDistance,
                                                  codeList=DistanceType)
        self.cfl_param = InputParamFrame(self.contours_fit_line_frame, "Param: ",
                                         yPos=2 * self.yDistance + 5, height=self.yDistance)
        self.cfl_reps = Slider_Input_Frame(self.contours_fit_line_frame, "Reps:",
                                                          yPos=3 * self.yDistance + 5, height=self.yDistance,
                                                          minValue=0, maxValue=0.5, resolution=0.0001,
                                                          button_up_cmd=self.sliderRelease)
        self.cfl_aeps = Slider_Input_Frame(self.contours_fit_line_frame, "Aeps:",
                                           yPos=4 * self.yDistance + 5, height=self.yDistance,
                                           minValue=0, maxValue=0.5, resolution=0.0001,
                                           button_up_cmd=self.sliderRelease)

    def setup_contours_approximation(self):
        self.contour_apprx_frame = VisionFrame(self)
        self.c_apprx_source_contour = SourceInput(self.contour_apprx_frame, "Source contours",
                                                  yPos=0 * self.yDistance + 5, height=self.yDistance,
                                                  maxStep=self.mainWindow.algorithmManager.maxStep)
        self.c_apprx_epsilon_percent = Slider_Input_Frame(self.contour_apprx_frame, "Epsilon percent: ",
                                                          yPos=1 * self.yDistance + 5, height=self.yDistance,
                                                          minValue=0, maxValue=0.5, resolution=0.0001,
                                                          button_up_cmd=self.sliderRelease)
        self.c_apprx_closed = CheckboxStepParamFrame(self.contour_apprx_frame, "Closed :",
                                                     yPos=2* self.yDistance + 5, height=self.yDistance)

    def setup_contour_linear_regression(self):
        self.contour_linear_regression_frame = VisionFrame(self)
        self.clr_contour_source = SourceInput(self.contour_linear_regression_frame, "Source contours",
                                              yPos=0 * self.yDistance + 5, height=self.yDistance,
                                              maxStep=self.mainWindow.algorithmManager.maxStep)
        self.clr_area_source = SourceInput(self.contour_linear_regression_frame, "Area source",
                                           yPos=1 * self.yDistance + 5, height=self.yDistance,
                                           maxStep=self.mainWindow.algorithmManager.maxStep)

    def setup_viet_ocr_frame(self):
        self.viet_ocr_frame = VisionFrame(self)
        model_list = ["vgg_seq2seq", "vgg_transformer"]
        self.vo_model = ComboForFlexibleValue(self.viet_ocr_frame, "Model: ",
                                              yPos=0 * self.yDistance + 5, height=self.yDistance,
                                              valueList=model_list)

        self.vo_weight_file = Select_Path_File(self.viet_ocr_frame, "Weight file:",
                                               yPos=1 * self.yDistance + 5, height=self.yDistance)
        device_list = ["cpu", "cuda:0", "cuda:1", "cuda:2"]
        self.vo_device = ComboForFlexibleValue(self.viet_ocr_frame, "Device: ",
                                               yPos=2 * self.yDistance + 5, height=self.yDistance,
                                               valueList=device_list)
        self.vo_vocab_file = Select_Path_File(self.viet_ocr_frame, "Vocab file:",
                                              yPos=3 * self.yDistance + 5, height=self.yDistance)

    def setupFloodFillFrame(self):
        self.floodFillFrame = VisionFrame(self)
        self.flood_fill_seed_point = Coordinate_Input(self.floodFillFrame, "Seed Point: ",
                                                      yPos=0 * self.yDistance + 5, height=self.yDistance)
        self.flood_fill_lowdiff = Slider_Input_Frame(self.floodFillFrame, "Low difference: ",
                                                     yPos=1 * self.yDistance + 5, height=self.yDistance,
                                                     minValue=0, maxValue=255, button_up_cmd=self.sliderRelease)
        self.flood_fill_updiff = Slider_Input_Frame(self.floodFillFrame, "Up difference: ",
                                                    yPos=2 * self.yDistance + 5, height=self.yDistance,
                                                    minValue=0, maxValue=255, button_up_cmd=self.sliderRelease)
        self.flood_fill_color = InputParamFrame(self.floodFillFrame, "Color: ",
                                                yPos=3 * self.yDistance + 5, height=self.yDistance)

    def setupReferenceEdgeCorner(self):
        self.referenceEdgeCornerFrame = VisionFrame(self)
        referenceType = ["Top", "Right", "Bottom", "Left", "Left Top", "Top Right", "Right Bottom", "Bottom Left"]
        self.rec_type = ComboForFixValue(self.referenceEdgeCornerFrame, "Type: ",
                                         yPos=0 * self.yDistance + 5, height=self.yDistance,
                                         codeList=ReferenceEdgeCornerType)

        # thresholdCode = [code.value for code in ThresholdCode]
        self.rec_thresh_type = ComboForFixValue(self.referenceEdgeCornerFrame, "Thresh Type: ", 1 * self.yDistance + 5,
                                                self.yDistance, codeList=ThresholdCode)

        self.rec_thresh = InputParamFrame(self.referenceEdgeCornerFrame, "Thresh:",
                                          yPos=2 * self.yDistance + 5, height=self.yDistance)

        self.rec_area = InputParamFrame(self.referenceEdgeCornerFrame, "Area contour:",
                                        yPos=3 * self.yDistance + 5, height=self.yDistance)

        self.rec_btn_get_reference_btn = VisionButton(self.referenceEdgeCornerFrame, text="Get reference",
                                                      command=self.click_rec_btn_get_reference_btn)

        self.rec_btn_get_reference_btn.place(x=5, y=4 * self.yDistance + 5, height=30)

    def click_rec_btn_get_reference_btn(self):
        if not self.saveValue():
            return
        self.mainWindow.researchingTab.currentAlgorithm.executeStep(self.stepParameter.stepId, isGettingReference=True)

    def setup_Measurand_conversion_frame(self):
        self.measuransCvtFrame = VisionFrame(self)

    def setup_gama_correction_frame(self):
        self.gama_correction_frame = VisionFrame(self)
        self.gama_corrention_value = Slider_Input_Frame(self.gama_correction_frame, "Value: ",
                                                        yPos=0 * self.yDistance + 5, height=self.yDistance,
                                                        minValue=0.1, maxValue=20, resolution=0.1,
                                                        button_up_cmd=self.sliderRelease)

    def setupHistogramEqualizationFrame(self):
        self.histogramEqualizationFrame = VisionFrame(self)

        typeList = ["Normal Equalization", "Adaptive Equalization"]
        self.his_equ_type = ComboForFlexibleValue(self.histogramEqualizationFrame, "Type: ",
                                                  yPos=0 * self.yDistance + 5, height=self.yDistance,
                                                  valueList=typeList)

        self.his_equ_clip_limit = Slider_Input_Frame(self.histogramEqualizationFrame, "Clip limit: ",
                                                     yPos=1 * self.yDistance + 5, height=self.yDistance,
                                                     minValue=1, maxValue=255, button_up_cmd=self.sliderRelease)
        self.his_equ_grid_size = Slider_Input_Frame(self.histogramEqualizationFrame, "Tile grid size: ",
                                                    yPos=2 * self.yDistance + 5, height=self.yDistance,
                                                    minValue=1, maxValue=255, button_up_cmd=self.sliderRelease)

    def setupBrightnessChangeFrame(self):
        self.brightness_change_frame = VisionFrame(self)
        typeList = ["Lighter", "Darker"]
        self.bright_change_type = ComboForFlexibleValue(self.brightness_change_frame, "Type: ",
                                                        yPos=0 * self.yDistance + 5, height=self.yDistance,
                                                        valueList=typeList)

        self.brightness_change_value = Slider_Input_Frame(self.brightness_change_frame, "Value: ",
                                                          yPos=1 * self.yDistance + 5, height=self.yDistance,
                                                          minValue=0, maxValue=255, button_up_cmd=self.sliderRelease)

    def setupRotateImageWithAngleFrame(self):
        self.rotateImageWithAngleFrame = VisionFrame(self)
        self.riwa_angle = InputParamFrame(self.rotateImageWithAngleFrame, "Angle: ", yPos=0 * self.yDistance + 5,
                                          height=self.yDistance)
        self.riwa_reshape = CheckboxStepParamFrame(self.rotateImageWithAngleFrame, "Reshape:",
                                                   yPos=1 * self.yDistance + 5, height=self.yDistance)

    def setup_ignore_area_frame(self):
        self.ignore_area_frame = VisionFrame(self)

    def setup_multi_select_area(self):
        self.multi_select_area_fr = VisionFrame(self)

    def show_ignore_area(self, area, area_type, area_id):
        imageShow = self.mainWindow.originalImage.copy()
        if area_type == "rectangle":
            cv.rectangle(imageShow, pt1=(area[0], area[1]), pt2=(area[2], area[3]), color=Color.cvBlue(),
                         thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                         lineType=cv.LINE_AA)
            cv.putText(imageShow, text=f"{area_id + 1}",
                       org=(int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2)),
                       color=Color.cvRed(),
                       thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                       fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                       fontFace=cv.FONT_HERSHEY_COMPLEX, lineType=cv.LINE_AA)
        elif area_type == "circle":
            cv.circle(imageShow, center=area[0],
                      radius=area[1],
                      color=Color.cvBlue(),
                      thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                      lineType=cv.LINE_AA)
            cv.putText(imageShow, text=f"{area_id + 1}",
                       org=area[0],
                       color=Color.cvRed(),
                       thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                       fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                       fontFace=cv.FONT_HERSHEY_COMPLEX, lineType=cv.LINE_AA)
        self.mainWindow.showImage(imageShow)

    def delete_ignore_areas(self, area_id):
        self.stepParameter.ignore_areas_list.pop(area_id)
        self.update_ignore_area_list(self.stepParameter.ignore_areas_list)
        self.show_all_ignore_area()

    def add_ignore_area(self, area, area_type="rectangle"):
        self.stepParameter.ignore_areas_list.append((area, area_type))
        self.update_ignore_area_list(self.stepParameter.ignore_areas_list)
        self.show_all_ignore_area()

    def update_ignore_area_list(self, ignore_list):
        for ignore_are in self.ignore_areas:
            ignore_are.place_forget()

        if self.btn_delete_all_ignore_areas is not None:
            self.btn_show_all_ignore_areas.place_forget()
            self.btn_delete_all_ignore_areas.place_forget()

        self.ignore_areas = []
        i = 0
        for i, area in enumerate(ignore_list):
            self.ignore_areas.append(IgnoreArea(self.ignore_area_frame, i, area=area, yPos=i * self.yDistance + 5,
                                                height=self.yDistance, show_cmd=self.show_ignore_area,
                                                delete_cmd=self.delete_ignore_areas))
        if self.btn_delete_all_ignore_areas is None:
            self.btn_show_all_ignore_areas = VisionButton(self.ignore_area_frame, text="Show All",
                                                          command=self.show_all_ignore_area)
            self.btn_delete_all_ignore_areas = VisionButton(self.ignore_area_frame, text="Delete All",
                                                            command=self.delete_all_ignore_area)

        if i != 0:
            self.btn_show_all_ignore_areas.place(x=150, y=(i + 1) * self.yDistance + 5)
            self.btn_delete_all_ignore_areas.place(x=250, y=(i + 1) * self.yDistance + 5)

    def show_all_ignore_area(self):
        imageShow = self.mainWindow.originalImage.copy()
        for area_id, (area, area_type) in enumerate(self.stepParameter.ignore_areas_list):
            if area_type == "rectangle":
                cv.rectangle(imageShow, pt1=(area[0], area[1]), pt2=(area[2], area[3]), color=Color.cvBlue(),
                             thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                             lineType=cv.LINE_AA)
                cv.putText(imageShow, text=f"{area_id + 1}",
                           org=(int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2)),
                           color=Color.cvRed(),
                           thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                           fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                           fontFace=cv.FONT_HERSHEY_COMPLEX, lineType=cv.LINE_AA)
            elif area_type == "circle":
                cv.circle(imageShow, center=area[0],
                          radius=area[1],
                          color=Color.cvBlue(),
                          thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                          lineType=cv.LINE_AA)
                cv.putText(imageShow, text=f"{area_id + 1}",
                           org=area[0],
                           color=Color.cvRed(),
                           thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                           fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                           fontFace=cv.FONT_HERSHEY_COMPLEX, lineType=cv.LINE_AA)
        self.mainWindow.showImage(imageShow)

    def show_select_area(self, area, area_type, area_id):
        imageShow = self.mainWindow.originalImage.copy()
        if area_type == "rectangle":
            cv.rectangle(imageShow, pt1=(area[0], area[1]), pt2=(area[2], area[3]), color=Color.cvBlue(),
                         thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                         lineType=cv.LINE_AA)
            cv.putText(imageShow, text=f"{area_id + 1}",
                       org=(int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2)),
                       color=Color.cvRed(),
                       thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                       fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                       fontFace=cv.FONT_HERSHEY_COMPLEX, lineType=cv.LINE_AA)
        elif area_type == "circle":
            cv.circle(imageShow, center=area[0],
                      radius=area[1],
                      color=Color.cvBlue(),
                      thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                      lineType=cv.LINE_AA)
            cv.putText(imageShow, text=f"{area_id + 1}",
                       org=area[0],
                       color=Color.cvRed(),
                       thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                       fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                       fontFace=cv.FONT_HERSHEY_COMPLEX, lineType=cv.LINE_AA)
        self.mainWindow.showImage(imageShow)

    def delete_all_ignore_area(self):
        self.stepParameter.ignore_areas_list = []
        self.update_ignore_area_list(self.stepParameter.ignore_areas_list)
        self.show_all_ignore_area()

    def add_select_area(self, area, area_type="rectangle"):
        self.stepParameter.select_areas_list.append((area, area_type))
        self.update_multi_select_area_list(self.stepParameter.select_areas_list)
        self.show_all_select_area()

    def delete_select_areas(self, area_id):
        self.stepParameter.select_areas_list.pop(area_id)
        self.update_multi_select_area_list(self.stepParameter.select_areas_list)
        self.show_all_select_area()

    def update_multi_select_area_list(self, select_list):
        for select_area in self.select_area_list:
            select_area.place_forget()

        if self.btn_delete_all_select_areas is not None:
            self.btn_show_all_select_areas.place_forget()
            self.btn_delete_all_select_areas.place_forget()

        self.select_area_list = []
        i = 0
        for i, area in enumerate(select_list):
            self.select_area_list.append(
                IgnoreArea(self.multi_select_area_fr, i, area=area, yPos=i * self.yDistance + 5,
                           height=self.yDistance, show_cmd=self.show_select_area, delete_cmd=self.delete_select_areas))
        if self.btn_delete_all_select_areas is None:
            self.btn_show_all_select_areas = VisionButton(self.multi_select_area_fr, text="Show All",
                                                          command=self.show_all_select_area)
            self.btn_delete_all_select_areas = VisionButton(self.multi_select_area_fr, text="Delete All",
                                                            command=self.delete_all_select_area)

        if i != 0:
            self.btn_show_all_select_areas.place(x=150, y=(i + 1) * self.yDistance + 5)
            self.btn_delete_all_select_areas.place(x=250, y=(i + 1) * self.yDistance + 5)

    def show_all_select_area(self):
        imageShow = self.mainWindow.originalImage.copy()
        for area_id, (area, area_type) in enumerate(self.stepParameter.select_areas_list):
            if area_type == "rectangle":
                cv.rectangle(imageShow, pt1=(area[0], area[1]), pt2=(area[2], area[3]), color=Color.cvBlue(),
                             thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                             lineType=cv.LINE_AA)
                cv.putText(imageShow, text=f"{area_id + 1}",
                           org=(int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2)),
                           color=Color.cvRed(),
                           thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                           fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                           fontFace=cv.FONT_HERSHEY_COMPLEX, lineType=cv.LINE_AA)
            elif area_type == "circle":
                cv.circle(imageShow, center=area[0],
                          radius=area[1],
                          color=Color.cvBlue(),
                          thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                          lineType=cv.LINE_AA)
                cv.putText(imageShow, text=f"{area_id + 1}",
                           org=area[0],
                           color=Color.cvRed(),
                           thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                           fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                           fontFace=cv.FONT_HERSHEY_COMPLEX, lineType=cv.LINE_AA)
        self.mainWindow.showImage(imageShow)

    def delete_all_select_area(self):
        self.stepParameter.select_areas_list = []
        self.update_multi_select_area_list(self.stepParameter.select_areas_list)
        self.show_all_select_area()

    def setup_ddk_scratch_dl_frame(self):
        self.ddk_scratch_dl_frame = VisionFrame(self)
        self.dl_thresh = InputParamFrame(self.ddk_scratch_dl_frame, "Thresh: ",
                                         yPos=0 * self.yDistance + 5, height=self.yDistance)
        self.dl_resizeWidth = InputParamFrame(self.ddk_scratch_dl_frame, "Resize width: ",
                                              yPos=1 * self.yDistance + 5, height=self.yDistance)
        self.dl_resizeHeight = InputParamFrame(self.ddk_scratch_dl_frame, "Resize height: ",
                                               yPos=2 * self.yDistance + 5, height=self.yDistance)

    def setup_angle_from_2_lines(self):
        self.angle_from_2_lines_frame = VisionFrame(self)

        self.af2l_point1_line1 = SourceInput(self.angle_from_2_lines_frame, "Point 1(Line 1)",
                                             yPos=1 * self.yDistance + 5, height=self.yDistance,
                                             maxStep=self.mainWindow.algorithmManager.maxStep)
        self.af2l_point2_line1 = SourceInput(self.angle_from_2_lines_frame, "Point 2(Line 1)",
                                             yPos=2 * self.yDistance + 5, height=self.yDistance,
                                             maxStep=self.mainWindow.algorithmManager.maxStep)
        self.af2l_point1_line2 = SourceInput(self.angle_from_2_lines_frame, "Point 1(Line 2)",
                                             yPos=3 * self.yDistance + 5, height=self.yDistance,
                                             maxStep=self.mainWindow.algorithmManager.maxStep)
        self.af2l_point2_line2 = SourceInput(self.angle_from_2_lines_frame, "Point 2(Line 2)",
                                             yPos=4 * self.yDistance + 5, height=self.yDistance,
                                             maxStep=self.mainWindow.algorithmManager.maxStep)

        self.af2l_valid_range = Range_Input(self.angle_from_2_lines_frame, "Valid Range:", yPos=5 * self.yDistance + 5,
                                            height=self.yDistance,
                                            minValue=-359, maxValue=360, resolution=0.1)

    def setup_distance_point_to_point_frame(self):
        self.distance_P2P_frame = VisionFrame(self)
        self.p2p_point1_source = SourceInput(self.distance_P2P_frame, "Source point 1: ",
                                             yPos=0 * self.yDistance + 5, height=self.yDistance,
                                             maxStep=self.mainWindow.algorithmManager.maxStep)

        self.p2p_point2_source = SourceInput(self.distance_P2P_frame, "Source point 2: ",
                                             yPos=1 * self.yDistance + 5, height=self.yDistance,
                                             maxStep=self.mainWindow.algorithmManager.maxStep)

        self.p2p_range = Range_Input(self.distance_P2P_frame, "Valid Range:", yPos=2 * self.yDistance + 5,
                                     height=self.yDistance,
                                     minValue=0, maxValue=1000, resolution=1)

    def setup_distance_point_to_line_frame(self):
        self.distance_P2L_frame = VisionFrame(self)
        self.p2l_point_source = SourceInput(self.distance_P2L_frame, "Source point: ",
                                            yPos=0 * self.yDistance + 5, height=self.yDistance,
                                            maxStep=self.mainWindow.algorithmManager.maxStep)

        self.p2l_point1_line_source = SourceInput(self.distance_P2L_frame, "Source point 1 of line: ",
                                                  yPos=1 * self.yDistance + 5, height=self.yDistance,
                                                  maxStep=self.mainWindow.algorithmManager.maxStep)

        self.p2l_point2_line_source = SourceInput(self.distance_P2L_frame, "Source point 2 of line: ",
                                                  yPos=2 * self.yDistance + 5, height=self.yDistance,
                                                  maxStep=self.mainWindow.algorithmManager.maxStep)

        self.p2l_range = Range_Input(self.distance_P2L_frame, "Valid Range:", yPos=3 * self.yDistance + 5,
                                     height=self.yDistance,
                                     minValue=0, maxValue=1000, resolution=1)

    def setup_threshold_average_frame(self):
        self.threshold_average_frame = VisionFrame(self)

        self.ta_brightness_reflection = InputParamFrame(self.threshold_average_frame, "Brightness reflection :",
                                                        yPos=0 * self.yDistance + 5, height=self.yDistance)

    def setup_change_color_frame(self):
        self.change_color_frame = VisionFrame(self)
        codeList = [code.value for code in ChangeColorCode]
        self.change_color_code = ComboForFlexibleValue(self.change_color_frame, lblText="Code", valueList=codeList,
                                                       yPos=5 + 1 * self.yDistance, height=self.yDistance)
        self.change_color_mask = SourceInput(self.change_color_frame, lblText="Source mask :",
                                             yPos=5 + 0 * self.yDistance, height=self.yDistance,
                                             maxStep=self.mainWindow.algorithmManager.maxStep)

    def setup_ocr_tesseract_Frame(self):
        self.ocr_tesseract_frame = VisionFrame(self)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        language_list = pytesseract.get_languages(config='')
        self.available_language = ComboForFlexibleValue(self.ocr_tesseract_frame, "Language:",
                                                        yPos=0 * self.yDistance + 5,
                                                        height=self.yDistance, valueList=language_list)

    def setupSplitChannelFrame(self):
        self.splitChannelFrame = VisionFrame(self)
        self.sc_channel_id = InputParamFrame(self.splitChannelFrame, "Channel ID :", yPos=0 * self.yDistance + 5,
                                             height=self.yDistance)

    def setupConnectionContourFrame(self):
        self.connectionContourFrame = VisionFrame(self)
        self.cc_size = InputParamFrame(self.connectionContourFrame, "Size :", yPos=0 * self.yDistance + 5,
                                       height=self.yDistance)
        self.cc_distance = InputParamFrame(self.connectionContourFrame, "Distance :", yPos=1 * self.yDistance + 5,
                                           height=self.yDistance)
        self.cc_location = InputParamFrame(self.connectionContourFrame, "Location :", yPos=2 * self.yDistance + 5,
                                           height=self.yDistance)

    def setupResizeFrame(self):
        self.resizeFrame = VisionFrame(self)
        self.rs_sizeX = InputParamFrame(self.resizeFrame, "Size X:", yPos=0 * self.yDistance + 5, height=self.yDistance)
        self.rs_sizeY = InputParamFrame(self.resizeFrame, "Size Y:", yPos=1 * self.yDistance + 5, height=self.yDistance)
        self.rs_ratio = CheckboxStepParamFrame(self.resizeFrame, "Using Ratio: ",
                                               yPos=3 * self.yDistance + 5, height=self.yDistance)
        self.rs_fX = InputParamFrame(self.resizeFrame, "Ratio fX: ",
                                     yPos=4 * self.yDistance + 5, height=self.yDistance)
        self.rs_fY = InputParamFrame(self.resizeFrame, "Ratio fY: ",
                                     yPos=5 * self.yDistance + 5, height=self.yDistance)

    def setupFindChessBoardCornersFrame(self):
        self.findChessBoardCornersFrame = VisionFrame(self)
        self.cbc_sizeX = InputParamFrame(self.findChessBoardCornersFrame, "size X(corners) :",
                                         yPos=0 * self.yDistance + 5, height=self.yDistance)
        self.cbc_sizeY = InputParamFrame(self.findChessBoardCornersFrame, "size Y(corners) :",
                                         yPos=1 * self.yDistance + 5, height=self.yDistance)

    def setupBarcodeReaderFrame(self):
        self.barcodeReaderFrame = VisionFrame(self)

    def setupDataMatrix2ReaderFrame(self):
        self.dataMatrixReaderFrame = VisionFrame(self)
        self.get_min_area_box = SourceInput(self.dataMatrixReaderFrame, 'Get min area',
                                              yPos=0 * self.yDistance + 5, height=self.yDistance,
                                              maxStep=self.mainWindow.algorithmManager.maxStep)

    def setupMinAreaRectFrame(self):
        self.minAreaRectFrame = VisionFrame(self)
        self.mar_source_contour = SourceInput(self.minAreaRectFrame, "Source contours",
                                              yPos=0 * self.yDistance + 5, height=self.yDistance,
                                              maxStep=self.mainWindow.algorithmManager.maxStep)

    def setupPaintFrame(self):
        self.paintFrame = VisionFrame(self)

        self.paintColorLbl = VisionLabel(self.paintFrame, text="Color(BGR): ")
        self.paintColorLbl.place(x=5, y=self.yDistance + 5)

        self.paintBlue = AdjustValueFrame(self.paintFrame, advancedCmd=None)
        self.paintBlue.place(x=100, y=self.yDistance + 5, width=70, height=25)

        self.paintGreen = AdjustValueFrame(self.paintFrame, advancedCmd=None)
        self.paintGreen.place(x=230, y=self.yDistance + 5, width=70, height=25)

        self.paintRed = AdjustValueFrame(self.paintFrame, advancedCmd=None)
        self.paintRed.place(x=360, y=self.yDistance + 5, width=70, height=25)

    def setupExtremeFrame(self):
        self.extremeFrame = VisionFrame(self)
        self.ge_contourInput = SourceInput(self.extremeFrame, "Contours input: ",
                                           yPos=0 * self.yDistance + 5, height=self.yDistance,
                                           maxStep=self.mainWindow.algorithmManager.maxStep)
        self.typeExtreme = ComboForFixValue(self.extremeFrame, "Type",
                                            codeList=RF_Type,
                                            yPos=1 * self.yDistance + 5, height=self.yDistance)

    def setupDrawCircleFrame(self):
        self.drawCircleFrame = VisionFrame(self)

        self.dc_inputCircle = SourceInput(self.drawCircleFrame, "Circle input", showCommand=None,
                                          yPos=0 * self.yDistance + 5, height=self.yDistance,
                                          maxStep=self.mainWindow.algorithmManager.maxStep)

        self.dc_centerX = InputParamFrame(self.drawCircleFrame, "Center X: ",
                                          yPos=1 * self.yDistance + 5, height=self.yDistance)
        self.dc_centerY = InputParamFrame(self.drawCircleFrame, "Center Y: ",
                                          yPos=2 * self.yDistance + 5, height=self.yDistance)
        self.dc_radius = InputParamFrame(self.drawCircleFrame, "Radius: ",
                                         yPos=3 * self.yDistance + 5, height=self.yDistance)
        self.dc_thickness = InputParamFrame(self.drawCircleFrame, "Thickness: ",
                                            yPos=4 * self.yDistance + 5, height=self.yDistance)

    def setupReferenceTranslation(self):
        self.refereneceTranslationFrame = VisionFrame(self)

        self.rt_baseSourceIndex = SourceInput(self.refereneceTranslationFrame, "Base process step: ",
                                              yPos=0 * self.yDistance + 5, height=self.yDistance,
                                              showCommand=self.clickBtnShowSourceImage,
                                              sourceImageName=SourceImageName.rt_baseSource,
                                              maxStep=self.mainWindow.algorithmManager.maxStep)
        self.rt_destSourceIndex = SourceInput(self.refereneceTranslationFrame, "Current process step: ",
                                              yPos=1 * self.yDistance + 5, height=self.yDistance,
                                              showCommand=self.clickBtnShowSourceImage,
                                              sourceImageName=SourceImageName.rt_currentSource,
                                              maxStep=self.mainWindow.algorithmManager.maxStep)
        self.rt_referenceType = ComboForFixValue(self.refereneceTranslationFrame, "type: ",
                                                 yPos=2 * self.yDistance + 5, height=self.yDistance, codeList=RF_Type)

    def setupTranslationMoveFrame(self):
        self.translationMoveFrame = VisionFrame(self)

        self.trans_move_x = InputParamFrame(self.translationMoveFrame, "Move X(Pixels): ", yPos=0 * self.yDistance + 5,
                                            height=self.yDistance)
        self.trans_move_y = InputParamFrame(self.translationMoveFrame, "Move Y(Pixels): ", yPos=1 * self.yDistance + 5,
                                            height=self.yDistance)

    def setupBSFrame(self):
        self.bsFrame = VisionFrame(self)
        #
        # stepList = []
        # stepList.append("Template")
        # stepList.append("None")
        # stepList.append("Original image")
        # for i in range(self.mainWindow.algorithmManager.maxStep):
        #     stepList.append("Step {}".format(i))

        self.bs_processImageIndex = SourceIdxCombo(self.bsFrame, "Process image: ", 0 * self.yDistance + 5,
                                                   self.yDistance, self.stepList, command=self.clickBtnShowSourceImage,
                                                   sourceImageName=SourceImageName.bs_processImage)

        self.bs_historyNum = InputParamFrame(self.bsFrame, "History frame number: ", yPos=1 * self.yDistance + 5,
                                             height=self.yDistance)
        self.bs_dist2Threshold = InputParamFrame(self.bsFrame, "Dist to threshold: ", yPos=2 * self.yDistance + 5,
                                                 height=self.yDistance)
        self.bs_detectShadows = CheckboxStepParamFrame(self.bsFrame, "Detect shadows: ", yPos=3 * self.yDistance + 5,
                                                       height=self.yDistance)

    def setupHoughLinesFrame(self):
        self.houghLinesFrame = VisionFrame(self)

        self.hl_rho = InputParamFrame(self.houghLinesFrame, "Rho(Pixel) :", yPos=0 * self.yDistance + 5,
                                      height=self.yDistance)
        self.hl_theta = InputParamFrame(self.houghLinesFrame, "Theta(Degrees) :", yPos=1 * self.yDistance + 5,
                                        height=self.yDistance)
        self.hl_threshold = InputParamFrame(self.houghLinesFrame, "Threshold(Intersections) :",
                                            yPos=2 * self.yDistance + 5, height=self.yDistance)
        self.hl_srn = InputParamFrame(self.houghLinesFrame, "Srn :", yPos=3 * self.yDistance + 5, height=self.yDistance)
        self.hl_stn = InputParamFrame(self.houghLinesFrame, "Stn :", yPos=4 * self.yDistance + 5, height=self.yDistance)
        self.hl_min_theta = InputParamFrame(self.houghLinesFrame, "Min theta(Degree) :", yPos=5 * self.yDistance + 5,
                                            height=self.yDistance)
        self.hl_max_theta = InputParamFrame(self.houghLinesFrame, "Max theta(Degree) :", yPos=6 * self.yDistance + 5,
                                            height=self.yDistance)
        self.hl_min_length = InputParamFrame(self.houghLinesFrame, "Min line length(pixel) :",
                                             yPos=7 * self.yDistance + 5, height=self.yDistance)
        self.hl_max_gap = InputParamFrame(self.houghLinesFrame, "Max gap(number) :", yPos=8 * self.yDistance + 5,
                                          height=self.yDistance)

    def setupFocusCheckingFrame(self):
        self.focusCheckingFrame = VisionFrame(self)
        self.focusThresh = InputParamFrame(self.focusCheckingFrame, "Focus thresh : ", yPos=0 * self.yDistance + 5,
                                           height=self.yDistance)

    def setupOriginalReferenceFrame(self):
        self.originalReferenceFrame = VisionFrame(self)
        stepList = []
        for i in range(self.mainWindow.algorithmManager.maxStep):
            stepList.append("Step {}".format(i))

        self.orRef1StepIdx = ComboForFlexibleValue(self.originalReferenceFrame, "Reference Point 1",
                                                   yPos=0 * self.yDistance + 5, height=self.yDistance,
                                                   valueList=stepList)
        self.orRef2StepIdx = ComboForFlexibleValue(self.originalReferenceFrame, "Reference Point 2",
                                                   yPos=1 * self.yDistance + 5, height=self.yDistance,
                                                   valueList=stepList)
        self.orRef3StepIdx = ComboForFlexibleValue(self.originalReferenceFrame, "Reference Point 3",
                                                   yPos=2 * self.yDistance + 5, height=self.yDistance,
                                                   valueList=stepList)

    def setupCannyFrame(self):
        self.cannyFrame = VisionFrame(self)
        self.cannyMinThresh = InputParamFrame(self.cannyFrame, lblText="Min thresh value: ",
                                              yPos=0 * self.yDistance + 5, height=self.yDistance)
        self.cannyMaxThresh = InputParamFrame(self.cannyFrame, lblText="Max thresh value: ",
                                              yPos=1 * self.yDistance + 5, height=self.yDistance)
        self.canny_kernel_size = InputParamFrame(self.cannyFrame, lblText="Kernel size: ", yPos=3 * self.yDistance + 5,
                                                 height=self.yDistance)

    def setupAdaptiveThresholdFrame(self):
        self.adaptiveThresholdFrame = VisionFrame(self)
        self.adaptiveThreshMaxVal = InputParamFrame(self.adaptiveThresholdFrame, lblText="Max value: ",
                                                    yPos=0 * self.yDistance + 5, height=self.yDistance)
        self.adaptiveMode = ComboForFixValue(self.adaptiveThresholdFrame, lblText="Adaptive mode: ",
                                             yPos=1 * self.yDistance + 5, height=self.yDistance,
                                             codeList=AdaptiveThreshMode)
        self.adaptiveBlockSize = InputParamFrame(self.adaptiveThresholdFrame, lblText="Block size: ",
                                                 yPos=2 * self.yDistance + 5, height=self.yDistance)
        self.adaptiveChangeVal = InputParamFrame(self.adaptiveThresholdFrame, lblText="Change value: ",
                                                 yPos=3 * self.yDistance + 5, height=self.yDistance)
        self.adaptiveThreshType = ComboForFixValue(self.adaptiveThresholdFrame, lblText="Thresh type: ",
                                                   yPos=4 * self.yDistance + 5, height=self.yDistance,
                                                   codeList=ThresholdCode)

    def setupBitWiseFrame(self):
        self.bitwiseFrame = VisionFrame(self)
        # stepList = []
        # stepList.append("Template")
        # stepList.append("None")
        # stepList.append("Original image")
        # for i in range(self.mainWindow.algorithmManager.maxStep):
        #     stepList.append("Step {}".format(i))

        self.sourceImage2 = SourceIdxCombo(self.bitwiseFrame, "Source image 2: ", 0 * self.yDistance + 5,
                                           self.yDistance, self.stepList, command=self.clickBtnShowSourceImage,
                                           sourceImageName=SourceImageName.sourceImage2)
        self.maskImage = SourceIdxCombo(self.bitwiseFrame, "mask: ", 1 * self.yDistance + 5,
                                        self.yDistance, self.stepList, command=self.clickBtnShowSourceImage,
                                        sourceImageName=SourceImageName.mask)

    def setupDilateAndErodeFrame(self):
        self.dilateFrame = VisionFrame(self)
        self.kernelSizeX = InputParamFrame(self.dilateFrame, "Kernel size X: ", 0 * self.yDistance + 5, self.yDistance)
        self.kernelSizeY = InputParamFrame(self.dilateFrame, "Kernel size Y: ", 1 * self.yDistance + 5, self.yDistance)
        self.iterations = InputParamFrame(self.dilateFrame, "Iterations: ", 2 * self.yDistance + 5, self.yDistance)

    def setupHoughCircleFrame(self):
        self.houghCircleSettingFrame = VisionFrame(self)
        self.minDistHoughCircle = Slider_Input_Frame(self.houghCircleSettingFrame, "Min Dist: ",
                                                     0 * self.yDistance + 5, self.yDistance,
                                                     minValue=1, maxValue=1000, button_up_cmd=self.sliderRelease)
        self.parm1HoughCircle = Slider_Input_Frame(self.houghCircleSettingFrame, "Parm 1: ", 1 * self.yDistance + 5,
                                                   self.yDistance,
                                                   minValue=1, maxValue=100, button_up_cmd=self.sliderRelease)
        self.parm2HoughCircle = Slider_Input_Frame(self.houghCircleSettingFrame, "Parm 2: ", 2 * self.yDistance + 5,
                                                   self.yDistance,
                                                   minValue=1, maxValue=100, button_up_cmd=self.sliderRelease)
        self.minRadiusHoughCircle = Slider_Input_Frame(self.houghCircleSettingFrame, "Min Radius: ",
                                                       3 * self.yDistance + 5, self.yDistance,
                                                       minValue=1, maxValue=2000, button_up_cmd=self.sliderRelease)
        self.maxRadiusHoughCircle = Slider_Input_Frame(self.houghCircleSettingFrame, "Max Radius: ",
                                                       4 * self.yDistance + 5, self.yDistance,
                                                       minValue=2, maxValue=2000, button_up_cmd=self.sliderRelease)
        self.betweenDistHoughCircle = Slider_Input_Frame(self.houghCircleSettingFrame, "Between dist: ",
                                                         5 * self.yDistance + 5, self.yDistance,
                                                         minValue=1, maxValue=2000, button_up_cmd=self.sliderRelease)
        self.trustNumberHoughCircle = InputParamFrame(self.houghCircleSettingFrame, "Trust number: ",
                                                      6 * self.yDistance + 5, self.yDistance)

    def setupThresholdFrame(self):
        self.thresholdFrame = VisionFrame(self)
        # Cvt color code
        thresholdCode = []
        for code in ThresholdCode:
            thresholdCode.append(code.name)
        self.threshold_thresh_val = Slider_Input_Frame(self.thresholdFrame, "Thresh Value:", 0 * self.yDistance + 5,
                                                       self.yDistance,
                                                       minValue=0, maxValue=255, button_up_cmd=self.sliderRelease)
        self.maxThresValueEntry = InputParamFrame(self.thresholdFrame, "Max Value: ", 1 * self.yDistance + 5,
                                                  self.yDistance)
        self.threshType1Combo = ComboxBoxStepParmFrame(self.thresholdFrame, "Thresh Type 1: ", 2 * self.yDistance + 5,
                                                       self.yDistance, valueList=thresholdCode, codeList=ThresholdCode)
        self.threshType2Combo = ComboxBoxStepParmFrame(self.thresholdFrame, "Thresh Type 2: ", 3 * self.yDistance + 5,
                                                       self.yDistance, valueList=thresholdCode, codeList=ThresholdCode)

    def setupFindContoursFrame(self):
        self.findContoursFrame = VisionFrame(self)
        self.contours_binarySource = SourceInput(self.findContoursFrame, "Binary Source: ",
                                                 yPos=0 * self.yDistance + 5, height=self.yDistance,
                                                 maxStep=self.mainWindow.algorithmManager.maxStep)
        self.contours_areaSource = SourceInput(self.findContoursFrame, "Area Source: ",
                                               yPos=1 * self.yDistance + 5, height=self.yDistance,
                                               maxStep=self.mainWindow.algorithmManager.maxStep)
        self.minContoursArea = Slider_Input_Frame(self.findContoursFrame, "Min Area: ", 2 * self.yDistance + 5,
                                                  self.yDistance, minValue=-1, maxValue=100000,
                                                  button_up_cmd=self.sliderRelease)

        # self.minContoursArea = InputParamFrame(self.findContoursFrame, "Min Area: ", 2 * self.yDistance + 5, self.yDistance)
        self.maxContoursArea = Slider_Input_Frame(self.findContoursFrame, "Max Area: ", 3 * self.yDistance + 5,
                                                  self.yDistance,
                                                  minValue=-1, maxValue=5472, button_up_cmd=self.sliderRelease)
        self.minContoursWidth = Slider_Input_Frame(self.findContoursFrame, "Min Width: ", 4 * self.yDistance + 5,
                                                   self.yDistance,
                                                   minValue=-1, maxValue=5472, button_up_cmd=self.sliderRelease)
        self.maxContoursWidth = Slider_Input_Frame(self.findContoursFrame, "Max Width: ", 5 * self.yDistance + 5,
                                                   self.yDistance,
                                                   minValue=-1, maxValue=5472, button_up_cmd=self.sliderRelease)
        self.minContoursHeight = Slider_Input_Frame(self.findContoursFrame, "Min Height: ", 6 * self.yDistance + 5,
                                                    self.yDistance,
                                                    minValue=-1, maxValue=5472, button_up_cmd=self.sliderRelease)
        self.maxContoursHeight = Slider_Input_Frame(self.findContoursFrame, "Max Height: ", 7 * self.yDistance + 5,
                                                    self.yDistance,
                                                    minValue=-1, maxValue=5472, button_up_cmd=self.sliderRelease)
        self.minAspectRatio = Slider_Input_Frame(self.findContoursFrame, "Min Aspect Ratio: ", 8 * self.yDistance + 5,
                                                 self.yDistance,
                                                 minValue=-1, maxValue=100, button_up_cmd=self.sliderRelease)
        self.maxAspectRatio = Slider_Input_Frame(self.findContoursFrame, "Max Aspect Ratio: ", 9 * self.yDistance + 5,
                                                 self.yDistance,
                                                 minValue=-1, maxValue=100, button_up_cmd=self.sliderRelease)
        self.numContourThresh = InputParamFrame(self.findContoursFrame, "Number Contours Thresh: ",
                                                10 * self.yDistance + 5, self.yDistance)

    def setupColorDetectFrame(self):
        self.colorDetectFrame = VisionFrame(self)

        # Base Color
        self.bgrCDToleranceLbl = VisionLabel(self.colorDetectFrame,
                                             text=self.mainWindow.languageManager.localized("baseColor"))
        self.bgrCDToleranceLbl.place(x=5, y=0)

        self.bToleranceLbl = VisionLabel(self.colorDetectFrame, text="B")
        self.bToleranceLbl.place(x=self.xDistance - 15, y=0)

        self.bCDBaseColorEntry = VisionEntry(self.colorDetectFrame)
        self.bCDBaseColorEntry.place(x=self.xDistance, y=0, width=35, height=20)

        self.gToleranceLbl = VisionLabel(self.colorDetectFrame, text="G")
        self.gToleranceLbl.place(x=self.xDistance + 80 - 15, y=0)
        self.gCDBaseColorEntry = VisionEntry(self.colorDetectFrame)
        self.gCDBaseColorEntry.place(x=self.xDistance + 80, y=0, width=35, height=20)

        self.rToleranceLbl = VisionLabel(self.colorDetectFrame, text="R")
        self.rToleranceLbl.place(x=self.xDistance + 160 - 15, y=0)
        self.rCDBaseColorEntry = VisionEntry(self.colorDetectFrame)
        self.rCDBaseColorEntry.place(x=self.xDistance + 160, y=0, width=35, height=20)

        # Range color tolerance
        self.bgrCDToleranceLbl = VisionLabel(self.colorDetectFrame,
                                             text=self.mainWindow.languageManager.localized("rgbTolerance"))
        self.bgrCDToleranceLbl.place(x=5, y=self.yDistance + 5)

        self.bCDToleranceLbl = VisionLabel(self.colorDetectFrame, text="B")
        self.bCDToleranceLbl.place(x=self.xDistance - 15, y=self.yDistance + 5)

        self.bCDToleranceEntry = VisionEntry(self.colorDetectFrame)
        self.bCDToleranceEntry.place(x=self.xDistance, y=self.yDistance + 5, width=35, height=20)

        self.gCDToleranceLbl = VisionLabel(self.colorDetectFrame, text="G")
        self.gCDToleranceLbl.place(x=self.xDistance + 80 - 15, y=self.yDistance + 5)
        self.gCDToleranceEntry = VisionEntry(self.colorDetectFrame)
        self.gCDToleranceEntry.place(x=self.xDistance + 80, y=self.yDistance + 5, width=35, height=20)

        self.rCDToleranceLbl = VisionLabel(self.colorDetectFrame, text="R")
        self.rCDToleranceLbl.place(x=self.xDistance + 160 - 15, y=self.yDistance + 5)
        self.rCDToleranceEntry = VisionEntry(self.colorDetectFrame)
        self.rCDToleranceEntry.place(x=self.xDistance + 160, y=self.yDistance + 5, width=35, height=20)

        self.countNonZeroThreshCD = InputParamFrame(self.colorDetectFrame,
                                                    self.mainWindow.languageManager.localized("nonzeroThresh"),
                                                    2 * self.yDistance + 5, self.yDistance)

    def setupHLSRangeFrame(self):
        self.hlsRangeFrame = VisionFrame(self)
        lowerLabel = VisionLabel(self.hlsRangeFrame, text="Lower", font=VisionFont.stepSettingFont())
        lowerLabel.place(x=90, y=0 * self.yDistance + 5)
        upperLabel = VisionLabel(self.hlsRangeFrame, text="Upper", font=VisionFont.stepSettingFont())
        upperLabel.place(x=220, y=0 * self.yDistance + 5)

        hLabel = VisionLabel(self.hlsRangeFrame, text="H : ", font=VisionFont.stepSettingFont())
        lLabel = VisionLabel(self.hlsRangeFrame, text="L : ", font=VisionFont.stepSettingFont())
        sLabel = VisionLabel(self.hlsRangeFrame, text="S : ", font=VisionFont.stepSettingFont())

        hLabel.place(x=5, y=self.yDistance + 5)
        lLabel.place(x=5, y=2 * self.yDistance + 5)
        sLabel.place(x=5, y=3 * self.yDistance + 5)

        self.hlsRangeFrame_HLower = AdjustValueFrame(self.hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hlsRangeFrame_HLower.place(x=80, y=self.yDistance + 5, width=70, height=25, )

        self.hlsRangeFrame_HUpper = AdjustValueFrame(self.hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hlsRangeFrame_HUpper.place(x=210, y=self.yDistance + 5, width=70, height=25)

        self.hlsRangeFrame_LLower = AdjustValueFrame(self.hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hlsRangeFrame_LLower.place(x=80, y=2 * self.yDistance + 5, width=70, height=25)

        self.hlsRangeFrame_LUpper = AdjustValueFrame(self.hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hlsRangeFrame_LUpper.place(x=210, y=2 * self.yDistance + 5, width=70, height=25)

        self.hlsRangeFrame_SLower = AdjustValueFrame(self.hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hlsRangeFrame_SLower.place(x=80, y=3 * self.yDistance + 5, width=70, height=25)

        self.hlsRangeFrame_SUpper = AdjustValueFrame(self.hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hlsRangeFrame_SUpper.place(x=210, y=3 * self.yDistance + 5, width=70, height=25)

        self.btnShowHLSImage = VisionButton(self.hlsRangeFrame, text="Show HLS image",
                                            command=self.clickBtnShowHLSImage, font=VisionFont.stepSettingFont())
        self.btnShowHLSImage.place(x=300, y=2 * self.yDistance + 5, width=120, height=30)

        self.hls_min_range = InputParamFrame(self.hlsRangeFrame, "Min range :", 5 * self.yDistance + 5, self.yDistance)
        self.hls_max_range = InputParamFrame(self.hlsRangeFrame, "Max range :", 6 * self.yDistance + 5, self.yDistance)

    def setupHSVRangeFrame(self):

        self.hsvRangeFrame = VisionFrame(self)
        lowerLabel = VisionLabel(self.hsvRangeFrame, text="Lower", font=VisionFont.stepSettingFont())
        lowerLabel.place(x=90, y=0 * self.yDistance + 5)
        upperLabel = VisionLabel(self.hsvRangeFrame, text="Upper", font=VisionFont.stepSettingFont())
        upperLabel.place(x=220, y=0 * self.yDistance + 5)

        hLabel = VisionLabel(self.hsvRangeFrame, text="H : ", font=VisionFont.stepSettingFont())
        sLabel = VisionLabel(self.hsvRangeFrame, text="S : ", font=VisionFont.stepSettingFont())
        vLabel = VisionLabel(self.hsvRangeFrame, text="V : ", font=VisionFont.stepSettingFont())

        hLabel.place(x=5, y=self.yDistance + 5)
        sLabel.place(x=5, y=2 * self.yDistance + 5)
        vLabel.place(x=5, y=3 * self.yDistance + 5)

        self.hsvRangeFrame_HLower = AdjustValueFrame(self.hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsvRangeFrame_HLower.place(x=80, y=self.yDistance + 5, width=70, height=25)

        self.hsvRangeFrame_HUpper = AdjustValueFrame(self.hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsvRangeFrame_HUpper.place(x=210, y=self.yDistance + 5, width=70, height=25)

        self.hsvRangeFrame_SLower = AdjustValueFrame(self.hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsvRangeFrame_SLower.place(x=80, y=2 * self.yDistance + 5, width=70, height=25)

        self.hsvRangeFrame_SUpper = AdjustValueFrame(self.hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsvRangeFrame_SUpper.place(x=210, y=2 * self.yDistance + 5, width=70, height=25)

        self.hsvRangeFrame_VLower = AdjustValueFrame(self.hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsvRangeFrame_VLower.place(x=80, y=3 * self.yDistance + 5, width=70, height=25)

        self.hsvRangeFrame_VUpper = AdjustValueFrame(self.hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsvRangeFrame_VUpper.place(x=210, y=3 * self.yDistance + 5, width=70, height=25)

        self.btnShowHSVImage = VisionButton(self.hsvRangeFrame, text="Show HSV image",
                                            command=self.clickBtnShowHSVImage, font=VisionFont.stepSettingFont())
        self.btnShowHSVImage.place(x=300, y=2 * self.yDistance + 5, width=120, height=30)
        self.hsv_min_range = InputParamFrame(self.hsvRangeFrame, "Min range :", 5 * self.yDistance + 5, self.yDistance)
        self.hsv_max_range = InputParamFrame(self.hsvRangeFrame, "Max range :", 6 * self.yDistance + 5, self.yDistance)

    def setupBGRRangeFrame(self):
        self.bgrRangeFrame = VisionFrame(self)
        lowerLabel = VisionLabel(self.bgrRangeFrame, text="Lower", font=VisionFont.stepSettingFont())
        lowerLabel.place(x=90, y=0 * self.yDistance + 5)
        upperLabel = VisionLabel(self.bgrRangeFrame, text="Upper", font=VisionFont.stepSettingFont())
        upperLabel.place(x=220, y=0 * self.yDistance + 5)

        bLabel = VisionLabel(self.bgrRangeFrame, text="B : ", font=VisionFont.stepSettingFont())
        gLabel = VisionLabel(self.bgrRangeFrame, text="G : ", font=VisionFont.stepSettingFont())
        rLabel = VisionLabel(self.bgrRangeFrame, text="R : ", font=VisionFont.stepSettingFont())

        bLabel.place(x=5, y=self.yDistance + 5)
        gLabel.place(x=5, y=2 * self.yDistance + 5)
        rLabel.place(x=5, y=3 * self.yDistance + 5)

        self.bgrRangeFrame_BLower = AdjustValueFrame(self.bgrRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgrRangeFrame_BLower.place(x=80, y=self.yDistance + 5, width=70, height=25)

        self.bgrRangeFrame_BUpper = AdjustValueFrame(self.bgrRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgrRangeFrame_BUpper.place(x=210, y=self.yDistance + 5, width=70, height=25)

        self.bgrRangeFrame_GLower = AdjustValueFrame(self.bgrRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgrRangeFrame_GLower.place(x=80, y=2 * self.yDistance + 5, width=70, height=25)

        self.bgrRangeFrame_GUpper = AdjustValueFrame(self.bgrRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgrRangeFrame_GUpper.place(x=210, y=2 * self.yDistance + 5, width=70, height=25)

        self.bgrRangeFrame_RLower = AdjustValueFrame(self.bgrRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgrRangeFrame_RLower.place(x=80, y=3 * self.yDistance + 5, width=70, height=25)

        self.bgrRangeFrame_RUpper = AdjustValueFrame(self.bgrRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgrRangeFrame_RUpper.place(x=210, y=3 * self.yDistance + 5, width=70, height=25)

        self.btnShowBgrImage = VisionButton(self.bgrRangeFrame, text="Show BGR image",
                                            command=self.clickBtnShowBgrImage, font=VisionFont.stepSettingFont())
        self.btnShowBgrImage.place(x=300, y=2 * self.yDistance + 5, width=120, height=30)

        self.bgr_min_range = InputParamFrame(self.bgrRangeFrame, "Min range :", 5 * self.yDistance + 5, self.yDistance)
        self.bgr_max_range = InputParamFrame(self.bgrRangeFrame, "Max range :", 6 * self.yDistance + 5, self.yDistance)

    def setupBGR_HLSRangeFrame(self):
        self.bgr_hlsRangeFrame = VisionFrame(self)
        lowerLabel = VisionLabel(self.bgr_hlsRangeFrame, text="Lower", font=VisionFont.stepSettingFont())
        lowerLabel.place(x=90, y=0 * self.yDistance + 5)
        upperLabel = VisionLabel(self.bgr_hlsRangeFrame, text="Upper", font=VisionFont.stepSettingFont())
        upperLabel.place(x=220, y=0 * self.yDistance + 5)

        bLabel = VisionLabel(self.bgr_hlsRangeFrame, text="B : ", font=VisionFont.stepSettingFont())
        gLabel = VisionLabel(self.bgr_hlsRangeFrame, text="G : ", font=VisionFont.stepSettingFont())
        rLabel = VisionLabel(self.bgr_hlsRangeFrame, text="R : ", font=VisionFont.stepSettingFont())

        bLabel.place(x=5, y=self.yDistance + 5)
        gLabel.place(x=5, y=2 * self.yDistance + 5)
        rLabel.place(x=5, y=3 * self.yDistance + 5)

        self.bgr_hlsRangeFrame_BLower = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_BLower.place(x=80, y=self.yDistance + 5, width=70, height=25)

        self.bgr_hlsRangeFrame_BUpper = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_BUpper.place(x=210, y=self.yDistance + 5, width=70, height=25)

        self.bgr_hlsRangeFrame_GLower = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_GLower.place(x=80, y=2 * self.yDistance + 5, width=70, height=25)

        self.bgr_hlsRangeFrame_GUpper = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_GUpper.place(x=210, y=2 * self.yDistance + 5, width=70, height=25)

        self.bgr_hlsRangeFrame_RLower = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_RLower.place(x=80, y=3 * self.yDistance + 5, width=70, height=25)

        self.bgr_hlsRangeFrame_RUpper = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_RUpper.place(x=210, y=3 * self.yDistance + 5, width=70, height=25)

        self.btnShowBgrImage = VisionButton(self.bgr_hlsRangeFrame, text="Show BGR image",
                                            command=self.clickBtnShowBgrImage, font=VisionFont.stepSettingFont())
        self.btnShowBgrImage.place(x=300, y=2 * self.yDistance + 5, width=120, height=30)

        hLabel = VisionLabel(self.bgr_hlsRangeFrame, text="H : ", font=VisionFont.stepSettingFont())
        lLabel = VisionLabel(self.bgr_hlsRangeFrame, text="L : ", font=VisionFont.stepSettingFont())
        sLabel = VisionLabel(self.bgr_hlsRangeFrame, text="S : ", font=VisionFont.stepSettingFont())

        hLabel.place(x=5, y=5 * self.yDistance + 5)
        lLabel.place(x=5, y=6 * self.yDistance + 5)
        sLabel.place(x=5, y=7 * self.yDistance + 5)

        self.bgr_hlsRangeFrame_HLower = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_HLower.place(x=80, y=5 * self.yDistance + 5, width=70, height=25)

        self.bgr_hlsRangeFrame_HUpper = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_HUpper.place(x=210, y=5 * self.yDistance + 5, width=70, height=25)

        self.bgr_hlsRangeFrame_LLower = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_LLower.place(x=80, y=6 * self.yDistance + 5, width=70, height=25)

        self.bgr_hlsRangeFrame_LUpper = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_LUpper.place(x=210, y=6 * self.yDistance + 5, width=70, height=25)

        self.bgr_hlsRangeFrame_SLower = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_SLower.place(x=80, y=7 * self.yDistance + 5, width=70, height=25)

        self.bgr_hlsRangeFrame_SUpper = AdjustValueFrame(self.bgr_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hlsRangeFrame_SUpper.place(x=210, y=7 * self.yDistance + 5, width=70, height=25)

        self.btnShowHLSImage = VisionButton(self.bgr_hlsRangeFrame, text="Show HLS image",
                                            command=self.clickBtnShowHLSImage, font=VisionFont.stepSettingFont())
        self.btnShowHLSImage.place(x=300, y=6 * self.yDistance + 5, width=120, height=30)

        self.bgr_hls_min_range = InputParamFrame(self.bgr_hlsRangeFrame, "Min range :", 9 * self.yDistance + 5,
                                                 self.yDistance)
        self.bgr_hls_max_range = InputParamFrame(self.bgr_hlsRangeFrame, "Max range :", 10 * self.yDistance + 5,
                                                 self.yDistance)

    def setupHSV_HLSRangeFrame(self):
        self.hsv_hlsRangeFrame = VisionFrame(self)
        lowerLabel = VisionLabel(self.hsv_hlsRangeFrame, text="Lower", font=VisionFont.stepSettingFont())
        lowerLabel.place(x=90, y=0 * self.yDistance + 5)
        upperLabel = VisionLabel(self.hsv_hlsRangeFrame, text="Upper", font=VisionFont.stepSettingFont())
        upperLabel.place(x=220, y=0 * self.yDistance + 5)

        hLabel = VisionLabel(self.hsv_hlsRangeFrame, text="H : ", font=VisionFont.stepSettingFont())
        sLabel = VisionLabel(self.hsv_hlsRangeFrame, text="S : ", font=VisionFont.stepSettingFont())
        vLabel = VisionLabel(self.hsv_hlsRangeFrame, text="V : ", font=VisionFont.stepSettingFont())

        hLabel.place(x=5, y=self.yDistance + 5)
        sLabel.place(x=5, y=2 * self.yDistance + 5)
        vLabel.place(x=5, y=3 * self.yDistance + 5)

        self.hsv_hlsRangeFrame_VHLower = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_VHLower.place(x=80, y=self.yDistance + 5, width=70, height=25)

        self.hsv_hlsRangeFrame_VHUpper = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_VHUpper.place(x=210, y=self.yDistance + 5, width=70, height=25)

        self.hsv_hlsRangeFrame_VSLower = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_VSLower.place(x=80, y=2 * self.yDistance + 5, width=70, height=25)

        self.hsv_hlsRangeFrame_VSUpper = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_VSUpper.place(x=210, y=2 * self.yDistance + 5, width=70, height=25)

        self.hsv_hlsRangeFrame_VVLower = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_VVLower.place(x=80, y=3 * self.yDistance + 5, width=70, height=25)

        self.hsv_hlsRangeFrame_VVUpper = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_VVUpper.place(x=210, y=3 * self.yDistance + 5, width=70, height=25)

        self.btnShowHSVImage = VisionButton(self.hsv_hlsRangeFrame, text="Show HSV image",
                                            command=self.clickBtnShowHSVImage, font=VisionFont.stepSettingFont())
        self.btnShowHSVImage.place(x=300, y=2 * self.yDistance + 5, width=120, height=30)

        hLabel = VisionLabel(self.hsv_hlsRangeFrame, text="H : ", font=VisionFont.stepSettingFont())
        lLabel = VisionLabel(self.hsv_hlsRangeFrame, text="L : ", font=VisionFont.stepSettingFont())
        sLabel = VisionLabel(self.hsv_hlsRangeFrame, text="S : ", font=VisionFont.stepSettingFont())

        hLabel.place(x=5, y=5 * self.yDistance + 5)
        lLabel.place(x=5, y=6 * self.yDistance + 5)
        sLabel.place(x=5, y=7 * self.yDistance + 5)

        self.hsv_hlsRangeFrame_SHLower = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_SHLower.place(x=80, y=5 * self.yDistance + 5, width=70, height=25)

        self.hsv_hlsRangeFrame_SHUpper = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_SHUpper.place(x=210, y=5 * self.yDistance + 5, width=70, height=25)

        self.hsv_hlsRangeFrame_SLLower = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_SLLower.place(x=80, y=6 * self.yDistance + 5, width=70, height=25)

        self.hsv_hlsRangeFrame_SLUpper = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_SLUpper.place(x=210, y=6 * self.yDistance + 5, width=70, height=25)

        self.hsv_hlsRangeFrame_SSLower = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_SSLower.place(x=80, y=7 * self.yDistance + 5, width=70, height=25)

        self.hsv_hlsRangeFrame_SSUpper = AdjustValueFrame(self.hsv_hlsRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.hsv_hlsRangeFrame_SSUpper.place(x=210, y=7 * self.yDistance + 5, width=70, height=25)

        self.btnShowHLSImage = VisionButton(self.hsv_hlsRangeFrame, text="Show HLS image",
                                            command=self.clickBtnShowHLSImage, font=VisionFont.stepSettingFont())
        self.btnShowHLSImage.place(x=300, y=6 * self.yDistance + 5, width=120, height=30)

        self.hsv_hls_min_range = InputParamFrame(self.hsv_hlsRangeFrame, "Min range :", 9 * self.yDistance + 5,
                                                 self.yDistance)
        self.hsv_hls_max_range = InputParamFrame(self.hsv_hlsRangeFrame, "Max range :", 10 * self.yDistance + 5,
                                                 self.yDistance)

    def setupBGR_HSVRangeFrame(self):
        self.bgr_hsvRangeFrame = VisionFrame(self)
        lowerLabel = VisionLabel(self.bgr_hsvRangeFrame, text="Lower", font=VisionFont.stepSettingFont())
        lowerLabel.place(x=90, y=0 * self.yDistance + 5)
        upperLabel = VisionLabel(self.bgr_hsvRangeFrame, text="Upper", font=VisionFont.stepSettingFont())
        upperLabel.place(x=220, y=0 * self.yDistance + 5)

        bLabel = VisionLabel(self.bgr_hsvRangeFrame, text="B : ", font=VisionFont.stepSettingFont())
        gLabel = VisionLabel(self.bgr_hsvRangeFrame, text="G : ", font=VisionFont.stepSettingFont())
        rLabel = VisionLabel(self.bgr_hsvRangeFrame, text="R : ", font=VisionFont.stepSettingFont())

        bLabel.place(x=5, y=self.yDistance + 5)
        gLabel.place(x=5, y=2 * self.yDistance + 5)
        rLabel.place(x=5, y=3 * self.yDistance + 5)

        self.bgr_hsvRangeFrame_BLower = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_BLower.place(x=80, y=self.yDistance + 5, width=70, height=25)

        self.bgr_hsvRangeFrame_BUpper = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_BUpper.place(x=210, y=self.yDistance + 5, width=70, height=25)

        self.bgr_hsvRangeFrame_GLower = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_GLower.place(x=80, y=2 * self.yDistance + 5, width=70, height=25)

        self.bgr_hsvRangeFrame_GUpper = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_GUpper.place(x=210, y=2 * self.yDistance + 5, width=70, height=25)

        self.bgr_hsvRangeFrame_RLower = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_RLower.place(x=80, y=3 * self.yDistance + 5, width=70, height=25)

        self.bgr_hsvRangeFrame_RUpper = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_RUpper.place(x=210, y=3 * self.yDistance + 5, width=70, height=25)

        self.btnShowBgrImage = VisionButton(self.bgr_hsvRangeFrame, text="Show BGR image",
                                            command=self.clickBtnShowBgrImage, font=VisionFont.stepSettingFont())
        self.btnShowBgrImage.place(x=300, y=2 * self.yDistance + 5, width=120, height=30)

        hLabel = VisionLabel(self.bgr_hsvRangeFrame, text="H : ", font=VisionFont.stepSettingFont())
        sLabel = VisionLabel(self.bgr_hsvRangeFrame, text="S : ", font=VisionFont.stepSettingFont())
        vLabel = VisionLabel(self.bgr_hsvRangeFrame, text="V : ", font=VisionFont.stepSettingFont())

        hLabel.place(x=5, y=5 * self.yDistance + 5)
        sLabel.place(x=5, y=6 * self.yDistance + 5)
        vLabel.place(x=5, y=7 * self.yDistance + 5)

        self.bgr_hsvRangeFrame_HLower = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_HLower.place(x=80, y=5 * self.yDistance + 5, width=70, height=25)

        self.bgr_hsvRangeFrame_HUpper = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_HUpper.place(x=210, y=5 * self.yDistance + 5, width=70, height=25)

        self.bgr_hsvRangeFrame_SLower = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_SLower.place(x=80, y=6 * self.yDistance + 5, width=70, height=25)

        self.bgr_hsvRangeFrame_SUpper = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_SUpper.place(x=210, y=6 * self.yDistance + 5, width=70, height=25)

        self.bgr_hsvRangeFrame_VLower = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_VLower.place(x=80, y=7 * self.yDistance + 5, width=70, height=25)

        self.bgr_hsvRangeFrame_VUpper = AdjustValueFrame(self.bgr_hsvRangeFrame, advancedCmd=self.clickBtnAdjustValue)
        self.bgr_hsvRangeFrame_VUpper.place(x=210, y=7 * self.yDistance + 5, width=70, height=25)

        self.btnShowHSVImage = VisionButton(self.bgr_hsvRangeFrame, text="Show HSV image",
                                            command=self.clickBtnShowHSVImage, font=VisionFont.stepSettingFont())
        self.btnShowHSVImage.place(x=300, y=6 * self.yDistance + 5, width=120, height=30)

        self.bgr_hsv_min_range = InputParamFrame(self.bgr_hsvRangeFrame, "Min range :", 9 * self.yDistance + 5,
                                                 self.yDistance)
        self.bgr_hsv_max_range = InputParamFrame(self.bgr_hsvRangeFrame, "Max range :", 10 * self.yDistance + 5,
                                                 self.yDistance)

    def clickBtnShowHSVImage(self):
        self.showConvertImage(key=cv.COLOR_BGR2HSV)

    def clickBtnShowHLSImage(self):
        self.showConvertImage(key=cv.COLOR_BGR2HLS)

    def clickBtnShowBgrImage(self):
        self.showConvertImage()

    def showConvertImage(self, key=None):
        sourceImage = None
        if not self.saveValue():
            return
        try:
            if self.stepParameter.resourceIndex[0] == -1:
                sourceImage = self.mainWindow.originalImage.copy()
            elif self.stepParameter.resourceIndex[0] == -4:
                refImagePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                       "/",
                                                       self.mainWindow.algorithmManager.currentName,
                                                       "/",
                                                       "imageReference_",
                                                       self.mainWindow.algorithmManager.getCurrentAlgorithm().algorithmParameter.refImageName,
                                                       ".png")
                try:
                    sourceImage = cv.imdecode(np.fromfile(refImagePath, dtype=np.uint8), cv.IMREAD_COLOR)
                except Exception as error:
                    text = "Please check the image reference. Detaial {}".format(error)
                    self.mainWindow.runningTab.insertLog(text)
                    messagebox.showerror("Show Reference Image",
                                         "Cannot read the Reference image. Please Add Reference Image first!")
            elif self.stepParameter.resourceIndex[0] == -3:
                templatePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                       "/",
                                                       self.mainWindow.algorithmManager.currentName,
                                                       "/",
                                                       "imageTemplate_",
                                                       self.stepParameter.templateName,
                                                       ".png")
                try:
                    sourceImage = cv.imdecode(np.fromfile(templatePath, dtype=np.uint8), cv.IMREAD_COLOR)
                except Exception as error:
                    text = "ERROR Please check the image template"
                    self.mainWindow.runningTab.insertLog(text)
                    messagebox.showerror("Show Template Image",
                                         "Cannot read the template image. Plase Add template first!")

            else:
                self.mainWindow.researchingTab.currentAlgorithm.executeStep(self.stepParameter.resourceIndex[0])
                sourceImage = self.mainWindow.researchingTab.currentAlgorithm.imageList[
                    self.stepParameter.resourceIndex[0]].copy()

            if sourceImage is None:
                messagebox.showerror("Show HSV image",
                                     "The image source has problem. Please check source image or source index!")
                self.mainWindow.runningTab.insertLog(
                    "ERROR Show HSV image: The image source has problem. Please check source image or source index!")
                return

            if self.stepParameter.workingArea is None:
                workingArea = (0, 0, sourceImage.shape[1], sourceImage.shape[0])
            else:
                workingArea = self.stepParameter.workingArea

            # validate working area:
            if workingArea[3] - workingArea[1] > sourceImage.shape[0] \
                    or workingArea[2] - workingArea[0] > sourceImage.shape[1] \
                    or workingArea[3] > sourceImage.shape[0] \
                    or workingArea[2] > sourceImage.shape[1]:
                messagebox.showerror("Show HSV image", "Working area out of image")
                return

            sourceImage = sourceImage[workingArea[1]:workingArea[3], workingArea[0]:workingArea[2]]
            if key is None:
                convertImage = sourceImage
            else:
                convertImage = ImageProcess.processCvtColor(sourceImage, key)

            self.mainWindow.showImage(convertImage)

        except Exception as error:
            messagebox.showerror("Show HSV image", "{}".format(error))
            self.mainWindow.runningTab.insertLog("ERROR Show HSV image: Detail: {}".format(error))

    def setupInRangeFrame(self):
        self.inRangeFrame = VisionFrame(self)

        # Base Color
        self.bgrToleranceLbl = VisionLabel(self.inRangeFrame,
                                           text=self.mainWindow.languageManager.localized("baseColor"))
        self.bgrToleranceLbl.place(x=5, y=0)

        self.bToleranceLbl = VisionLabel(self.inRangeFrame, text="B")
        self.bToleranceLbl.place(x=self.xDistance - 15, y=0)

        self.bIRBaseColorEntry = VisionEntry(self.inRangeFrame)
        self.bIRBaseColorEntry.place(x=self.xDistance, y=0, width=35, height=20)

        self.gToleranceLbl = VisionLabel(self.inRangeFrame, text="G")
        self.gToleranceLbl.place(x=self.xDistance + 80 - 15, y=0)
        self.gIRBaseColorEntry = VisionEntry(self.inRangeFrame)
        self.gIRBaseColorEntry.place(x=self.xDistance + 80, y=0, width=35, height=20)

        self.rToleranceLbl = VisionLabel(self.inRangeFrame, text="R")
        self.rToleranceLbl.place(x=self.xDistance + 160 - 15, y=0)
        self.rIRBaseColorEntry = VisionEntry(self.inRangeFrame)
        self.rIRBaseColorEntry.place(x=self.xDistance + 160, y=0, width=35, height=20)

        # Range color tolerance
        self.bgrToleranceLbl = VisionLabel(self.inRangeFrame,
                                           text=self.mainWindow.languageManager.localized("rgbTolerance"))
        self.bgrToleranceLbl.place(x=5, y=self.yDistance + 5)

        self.bToleranceLbl = VisionLabel(self.inRangeFrame, text="B")
        self.bToleranceLbl.place(x=self.xDistance - 15, y=self.yDistance + 5)

        self.bIRToleranceEntry = VisionEntry(self.inRangeFrame)
        self.bIRToleranceEntry.place(x=self.xDistance, y=self.yDistance + 5, width=35, height=20)

        self.gToleranceLbl = VisionLabel(self.inRangeFrame, text="G")
        self.gToleranceLbl.place(x=self.xDistance + 80 - 15, y=self.yDistance + 5)
        self.gIRToleranceEntry = VisionEntry(self.inRangeFrame)
        self.gIRToleranceEntry.place(x=self.xDistance + 80, y=self.yDistance + 5, width=35, height=20)

        self.rToleranceLbl = VisionLabel(self.inRangeFrame, text="R")
        self.rToleranceLbl.place(x=self.xDistance + 160 - 15, y=self.yDistance + 5)
        self.rIRToleranceEntry = VisionEntry(self.inRangeFrame)
        self.rIRToleranceEntry.place(x=self.xDistance + 160, y=self.yDistance + 5, width=35, height=20)

    def showBaseColor(self):
        self.bCDBaseColorEntry.delete(0, END)
        self.bCDBaseColorEntry.insert(0, "{}".format(int(float(self.stepParameter.averageColor[0]))))

        self.gCDBaseColorEntry.delete(0, END)
        self.gCDBaseColorEntry.insert(0, "{}".format(int(float(self.stepParameter.averageColor[1]))))

        self.rCDBaseColorEntry.delete(0, END)
        self.rCDBaseColorEntry.insert(0, "{}".format(int(float(self.stepParameter.averageColor[2]))))

        self.bIRBaseColorEntry.delete(0, END)
        self.bIRBaseColorEntry.insert(0, "{}".format(int(float(self.stepParameter.averageColor[0]))))

        self.gIRBaseColorEntry.delete(0, END)
        self.gIRBaseColorEntry.insert(0, "{}".format(int(float(self.stepParameter.averageColor[1]))))

        self.rIRBaseColorEntry.delete(0, END)
        self.rIRBaseColorEntry.insert(0, "{}".format(int(float(self.stepParameter.averageColor[2]))))

    def setAverageColor(self, color):
        chanel1, chanel2, chanel3 = color

        if self.stepParameter.stepAlgorithmName == MethodList.hsvInRange.value:
            self.hsvRangeFrame_HLower.setValue(chanel1 - 10)
            self.hsvRangeFrame_SLower.setValue(chanel2 - 10)
            self.hsvRangeFrame_VLower.setValue(chanel3 - 10)

            self.hsvRangeFrame_HUpper.setValue(chanel1 + 10)
            self.hsvRangeFrame_SUpper.setValue(chanel2 + 10)
            self.hsvRangeFrame_VUpper.setValue(chanel3 + 10)

        elif self.stepParameter.stepAlgorithmName == MethodList.hlsInRange.value:
            self.hlsRangeFrame_HLower.setValue(chanel1 - 10)
            self.hlsRangeFrame_LLower.setValue(chanel2 - 10)
            self.hlsRangeFrame_SLower.setValue(chanel3 - 10)

            self.hlsRangeFrame_HUpper.setValue(chanel1 + 10)
            self.hlsRangeFrame_LUpper.setValue(chanel2 + 10)
            self.hlsRangeFrame_SUpper.setValue(chanel3 + 10)

    def setupRotateFrame(self):
        self.rotateFrame = VisionFrame(self)
        self.rotateCode = ComboForFixValue(self.rotateFrame, "Rotate code: ", yPos=0 * self.yDistance + 5,
                                           height=self.yDistance, codeList=ImageRotate)
        self.rt_angle = InputParamFrame(self.rotateFrame, "Angle(degrees): ", yPos=1 * self.yDistance + 5,
                                        height=self.yDistance)
        self.rt_centerX = InputParamFrame(self.rotateFrame, "Center X: ", yPos=2 * self.yDistance + 5,
                                          height=self.yDistance)
        self.rt_centerY = InputParamFrame(self.rotateFrame, "Center Y: ", yPos=3 * self.yDistance + 5,
                                          height=self.yDistance)

    def setupFlipFrame(self):
        self.flipFrame = VisionFrame(self)
        self.flipCode = ComboForFixValue(self.flipFrame, "Flip code: ", yPos=0 * self.yDistance + 5,
                                         height=self.yDistance, codeList=ImageFlip)

    def setupCountNonzeroFrame(self):
        self.countNonzeroFame = VisionFrame(self)
        # nonzero thresh
        self.nonzero_min_range = InputParamFrame(self.countNonzeroFame, "Min range :", 0 * self.yDistance + 5,
                                                 self.yDistance)
        self.nonzero_max_range = InputParamFrame(self.countNonzeroFame, "Max range :", 1 * self.yDistance + 5,
                                                 self.yDistance)

    def setupCvtColorFrame(self):
        self.cvtColorFrame = VisionFrame(self)
        cvtColorCodeList = []
        for code in CvtColorCode:
            cvtColorCodeList.append(code.name)
        self.cvtColorCode = ComboxBoxStepParmFrame(self.cvtColorFrame, "Cvt color code: ", yPos=0 * self.yDistance + 5,
                                                   height=self.yDistance, valueList=cvtColorCodeList,
                                                   codeList=CvtColorCode)

    def setupMedianBlurFrame(self):
        self.medianBlurFrame = VisionFrame(self)
        self.blurSize = InputParamFrame(self.medianBlurFrame, "Blur size", yPos=0 * self.yDistance + 5,
                                        height=self.yDistance)
        self.blurSigmaX = InputParamFrame(self.medianBlurFrame, "Sigma X", yPos=1 * self.yDistance + 5,
                                          height=self.yDistance)

    def setupMatchingTemplateFrame(self):
        self.matchingTemplateFrame = VisionFrame(self)

        self.minMatchingValue = InputParamFrame(self.matchingTemplateFrame, "Min matching value: ", yPos=0,
                                                height=self.yDistance)
        self.multiMatching = CheckboxStepParamFrame(self.matchingTemplateFrame, "Multi matching: ", yPos=self.yDistance,
                                                    height=self.yDistance)
        self.sourceInput = SourceInput(self.matchingTemplateFrame, "Source Input: ", yPos=2 * self.yDistance,
                                       height=self.yDistance,
                                       maxStep=self.mainWindow.algorithmManager.maxStep)

    def setupParameterFrame(self):
        yDistance = 30
        xDistance = 150
        # self.stepList = []
        # self.stepList.append("Template")
        # self.stepList.append("None")
        # self.stepList.append("Original Image")
        # for i in range(self.mainWindow.algorithmManager.maxStep):
        #     self.stepList.append("Step {}".format(i))

        # source image index
        # self.resourceImageIndex = SourceIdxCombo(self, "Source Image",yPos=5, height=yDistance, valueList=self.stepList,
        #                                          command=self.clickBtnShowSourceImage, sourceImageName=SourceImageName.sourceImage)
        self.resourceImageIndex = SourceInput(self, "Source Image",
                                              showCommand=self.clickBtnShowSourceImage,
                                              yPos=5, height=yDistance, combo_width=100, xDistance=100,
                                              maxStep=self.mainWindow.algorithmManager.maxStep)
        # self.sourceImageLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("sourceImage"))
        # self.sourceImageLabel.place(x=5, y=5)
        # self.sourceImageCombobox = ttk.Combobox(self, value=self.stepList, state="readonly")
        # self.sourceImageCombobox.place(x=xDistance, y=5, width=150)
        # self.sourceImageCombobox.current(0)

    def setupButton(self):
        # self.btnRemoveWorkingArea = VisionButton(self, text = "Remove working area", font=VisionFont.stepSettingFont(), command=self.clickBtnRemoveWorkingArea)
        # self.btnRemoveWorkingArea.place(x=2*self.xDistance + 10, y=0, width=150, height=30)

        self.executeButton = ExecuteButton(self, command=self.clickBtnExecute)
        self.executeButton.place(relx=0.68, rely=0.8, relwidth=0.25, relheight=0.08)

        self.showAreaButton = ShowAreaButton(self, command=self.clickBtnShowWorkingArea)
        self.showAreaButton.place(relx=0.06, rely=0.8, relwidth=0.25, relheight=0.08)

        self.eraseAreaButton = EraseAreaButton(self, command=self.clickBtnRemoveWorkingArea)
        self.eraseAreaButton.place(relx=0.37, rely=0.8, relwidth=0.25, relheight=0.08)

        self.btnShowOriginalImage = ShowOriginButton(self, command=self.mainWindow.showOriginalImage)
        self.btnShowOriginalImage.place(relx=0.06, rely=0.9, relwidth=0.25, relheight=0.08)

        self.okButton = OkButton(self, command=self.clickBtnOK)
        self.okButton.place(relx=0.37, rely=0.9, relwidth=0.25, relheight=0.08)

        self.exitButton = CancelButton(self, command=self.clickBtnExit)
        self.exitButton.place(relx=0.68, rely=0.9, relwidth=0.25, relheight=0.08)

    def clickBtnShowSourceImage(self, sourceInput, sourceImageName: SourceImageName):
        self.mainWindow.resetBasePoint()
        try:
            if len(sourceInput) < 1:
                sourceIndex = sourceInput
            else:
                sourceIndex = sourceInput[0]
        except:
            sourceIndex = sourceInput

        sourceImage = None
        if sourceIndex == -1:
            if self.mainWindow.originalImage is None:
                messagebox.showerror("Original Image", "Please take or choose the image first!")
                return
            sourceImage = self.mainWindow.originalImage.copy()
        elif sourceIndex == -4:
            refImagePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                   "/",
                                                   self.mainWindow.algorithmManager.currentName,
                                                   "/",
                                                   "imageReference_",
                                                   self.mainWindow.algorithmManager.getCurrentAlgorithm().algorithmParameter.refImageName,
                                                   ".png")
            try:
                sourceImage = cv.imdecode(np.fromfile(refImagePath, dtype=np.uint8), cv.IMREAD_COLOR)
            except Exception as error:
                text = "Please check the image reference. Detaial {}".format(error)
                self.mainWindow.runningTab.insertLog(text)
                messagebox.showerror("Show Reference Image",
                                     "Cannot read the Reference image. Please Add Reference Image first!")
        elif sourceIndex == -3:
            templatePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                   "/",
                                                   self.mainWindow.algorithmManager.currentName,
                                                   "/",
                                                   "imageTemplate_",
                                                   self.stepParameter.templateName,
                                                   ".png")
            try:
                sourceImage = cv.imdecode(np.fromfile(templatePath, dtype=np.uint8), cv.IMREAD_COLOR)
            except Exception as error:
                text = "ERROR Please check the image template"
                self.mainWindow.runningTab.insertLog(text)
                messagebox.showerror("Show Template Image", "Cannot read the template image. Plase Add template first!")
        else:
            self.mainWindow.researchingTab.currentAlgorithm.executeStep(sourceIndex)
            sourceImage = self.mainWindow.researchingTab.currentAlgorithm.imageList[sourceIndex].copy()

        if sourceImage is None:
            return

        sourceWorkingArea = None
        if sourceImageName == SourceImageName.bs_processImage:
            sourceWorkingArea = self.stepParameter.bs_processWorkingArea
        elif sourceImageName == SourceImageName.sourceImage:
            sourceWorkingArea = self.stepParameter.workingArea
        elif sourceImageName == SourceImageName.rt_currentSource:
            sourceWorkingArea = self.stepParameter.rt_currentWorkingArea
        elif sourceImageName == SourceImageName.rt_baseSource:
            sourceWorkingArea = self.stepParameter.rt_baseWorkingArea

        if sourceWorkingArea is None:
            workingArea = (0, 0, sourceImage.shape[1], sourceImage.shape[0])
        else:
            workingArea = sourceWorkingArea

        # validate working area:
        if workingArea[3] - workingArea[1] > sourceImage.shape[0] \
                or workingArea[2] - workingArea[0] > sourceImage.shape[1] \
                or workingArea[3] > sourceImage.shape[0] \
                or workingArea[2] > sourceImage.shape[1]:
            # messagebox.showerror("Step {}".format(step.stepId),
            #                      "Step {} has working area out of image".format(step.stepId))
            text = "ERROR working area out of image"

            self.mainWindow.runningTab.insertLog(text)
            messagebox.showerror("Show working image", text)
            return

        sourceImage = sourceImage[workingArea[1]:workingArea[3],
                      workingArea[0]:workingArea[2]]
        self.mainWindow.showImage(sourceImage)

    def clickBtnShowWorkingArea(self, stepParameter=None):
        self.mainWindow.resetBasePoint()

        if stepParameter is not None:
            self.stepParameter = stepParameter
            sourceIndex, paramName = self.stepParameter.resourceIndex
        else:
            sourceIndex, paramName = self.resourceImageIndex.getValue()
        sourceImage = None

        if sourceIndex == -1:
            if self.mainWindow.originalImage is None:
                messagebox.showerror("Original Image", "Please take or choose the image first!")
                return
            sourceImage = self.mainWindow.originalImage.copy()

        elif sourceIndex == -4:
            refImagePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                   "/",
                                                   self.mainWindow.algorithmManager.currentName,
                                                   "/",
                                                   "imageReference_",
                                                   self.mainWindow.algorithmManager.getCurrentAlgorithm().algorithmParameter.refImageName,
                                                   ".png")
            try:
                sourceImage = cv.imdecode(np.fromfile(refImagePath, dtype=np.uint8), cv.IMREAD_COLOR)
            except Exception as error:
                text = "Please check the image reference. Detaial {}".format(error)
                self.mainWindow.runningTab.insertLog(text)
                messagebox.showerror("Show Reference Image",
                                     "Cannot read the Reference image. Please Add Reference Image first!")
        elif sourceIndex == -3:
            templatePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                   "/",
                                                   self.mainWindow.algorithmManager.currentName,
                                                   "/",
                                                   "imageTemplate_",
                                                   self.stepParameter.templateName,
                                                   ".png")
            try:
                sourceImage = cv.imdecode(np.fromfile(templatePath, dtype=np.uint8), cv.IMREAD_COLOR)
            except Exception as error:
                text = "ERROR Please check the image template"
                self.mainWindow.runningTab.insertLog(text)
                messagebox.showerror("Show Template Image", "Cannot read the template image. Plase Add template first!")
        else:
            self.mainWindow.researchingTab.currentAlgorithm.executeStep(sourceIndex)
            sourceImage = self.mainWindow.researchingTab.currentAlgorithm.imageList[sourceIndex].copy()

        if sourceImage is None:
            return

        if self.stepParameter.workingArea is None:
            workingArea = (0, 0, sourceImage.shape[1], sourceImage.shape[0])
        else:
            workingArea = self.stepParameter.workingArea

        # validate working area:
        if workingArea[3] - workingArea[1] > sourceImage.shape[0] \
                or workingArea[2] - workingArea[0] > sourceImage.shape[1] \
                or workingArea[3] > sourceImage.shape[0] \
                or workingArea[2] > sourceImage.shape[1]:
            text = "ERROR working area out of image"

            self.mainWindow.runningTab.insertLog(text)
            messagebox.showerror("Show working image", text)
            return
        try:
            cv.rectangle(sourceImage, (workingArea[0], workingArea[1]), (workingArea[2], workingArea[3]), (0, 255, 0),
                         self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, cv.LINE_AA)
            self.mainWindow.showImage(sourceImage)
        except Exception as error:
            text = "ERROR show working image area. Detail : {}".format(error)
            self.mainWindow.runningTab.insertLog(text)
            messagebox.showerror("Show working area", text)

    def clickBtnRemoveWorkingArea(self):
        self.stepParameter.workingArea = None

    def sliderRelease(self, value):
        self.clickBtnExecute()

    def clickBtnAdjustValue(self):
        self.clickBtnExecute()

    def clickBtnExecute(self):
        if not self.saveValue():
            return
        self.mainWindow.researchingTab.currentAlgorithm.executeStep(self.stepParameter.stepId)

    def clickBtnOK(self):
        if not self.saveValue():
            return
        self.okFlag = True
        self.masterWin.settingStepDone()

    def saveValue(self):
        try:
            # self.stepParameter.resourceIndex = self.sourceImageCombobox.current() - 3
            self.stepParameter.resourceIndex = self.resourceImageIndex.getValue()
            # Hough circle
            if self.stepParameter.stepAlgorithmName == MethodList.houghCircle.value \
                    or self.stepParameter.stepAlgorithmName == MethodList.averageHoughCircle.value:
                self.stepParameter.houghCircleMinDist = self.minDistHoughCircle.getIntValue()
                self.stepParameter.houghCircleParm1 = self.parm1HoughCircle.getIntValue()
                self.stepParameter.houghCircleParm2 = self.parm2HoughCircle.getIntValue()
                self.stepParameter.houghCircleMinRadius = self.minRadiusHoughCircle.getIntValue()
                self.stepParameter.houghCircleMaxRadius = self.maxRadiusHoughCircle.getIntValue()
                self.stepParameter.houghCircleBetweenDist = self.betweenDistHoughCircle.getIntValue()
                self.stepParameter.houghCircleTrustNumber = self.trustNumberHoughCircle.getIntValue()

            # Rotate image with angle
            elif self.stepParameter.stepAlgorithmName == MethodList.rotate_with_angle.value:
                self.stepParameter.riwa_angle = self.riwa_angle.getFloatValue()
                self.stepParameter.riwa_reshape = self.riwa_reshape.getValue()
            # Threshold
            elif self.stepParameter.stepAlgorithmName == MethodList.threshold.value:
                self.stepParameter.threshold_thresh_val = self.threshold_thresh_val.getValue()
                self.stepParameter.maxThresholdValue = self.maxThresValueEntry.getIntValue()
                if self.threshType1Combo.getValue() == ThresholdCode._None.value:
                    messagebox.showwarning("Thresh type 1", "Thresh type 1 cannot be None")
                    return False

                self.stepParameter.thresholdType1 = self.threshType1Combo.getValue()
                self.stepParameter.thresholdType2 = self.threshType2Combo.getValue()

            # in range
            elif self.stepParameter.stepAlgorithmName == MethodList.inRange.value:
                self.stepParameter.bgrToleranceRange = [int(float(self.bIRToleranceEntry.get())),
                                                        int(float(self.gIRToleranceEntry.get())),
                                                        int(float(self.rIRToleranceEntry.get()))]

                self.stepParameter.averageColor = [int(float(self.bIRBaseColorEntry.get())),
                                                   int(float(self.gIRBaseColorEntry.get())),
                                                   int(float(self.rIRBaseColorEntry.get()))]
            # Count nonzero
            elif self.stepParameter.stepAlgorithmName == MethodList.countNonzero.value:
                # self.stepParameter.nonzeroThresh = self.countNonZeroThresh.getIntValue()
                self.stepParameter.minRange = self.nonzero_min_range.getIntValue()
                self.stepParameter.maxRange = self.nonzero_max_range.getIntValue()
            # convert color
            elif self.stepParameter.stepAlgorithmName == MethodList.cvtColor.value:
                self.stepParameter.cvtColorCode = self.cvtColorCode.getValue()
            # Blur
            elif self.stepParameter.stepAlgorithmName == MethodList.medianBlur.value \
                    or self.stepParameter.stepAlgorithmName == MethodList.gaussianBlur.value \
                    or self.stepParameter.stepAlgorithmName == MethodList.blur.value:
                self.stepParameter.blurSize = self.blurSize.getIntValue()
                self.stepParameter.blurSigmaX = self.blurSigmaX.getIntValue()
            # Matching template
            elif self.stepParameter.stepAlgorithmName == MethodList.matchingTemplate.value:
                self.stepParameter.minMatchingValue = self.minMatchingValue.getFloatValue()
                self.stepParameter.multiMatchingFlag = self.multiMatching.getValue()
            # Detect color
            elif self.stepParameter.stepAlgorithmName == MethodList.colorDetect.value:
                self.stepParameter.bgrToleranceRange = [int(float(self.bCDToleranceEntry.get())),
                                                        int(float(self.gCDToleranceEntry.get())),
                                                        int(float(self.rCDToleranceEntry.get()))]

                self.stepParameter.averageColor = [int(float(self.bCDBaseColorEntry.get())),
                                                   int(float(self.gCDBaseColorEntry.get())),
                                                   int(float(self.rCDBaseColorEntry.get()))]

                self.stepParameter.nonzeroThresh = self.countNonZeroThreshCD.getIntValue()
            # find contours, fill contour, image from contour
            elif self.stepParameter.stepAlgorithmName == MethodList.findContour.value \
                    or self.stepParameter.stepAlgorithmName == MethodList.fillContour.value \
                    or self.stepParameter.stepAlgorithmName == MethodList.getImageInsideContour.value \
                    or self.stepParameter.stepAlgorithmName == MethodList.countContour.value:
                self.stepParameter.contours_area_source = self.contours_areaSource.getValue()
                self.stepParameter.contours_binary_source = self.contours_binarySource.getValue()
                self.stepParameter.minAreaContours = self.minContoursArea.getIntValue()
                self.stepParameter.maxAreaContours = self.maxContoursArea.getIntValue()
                self.stepParameter.minWidthContours = self.minContoursWidth.getIntValue()
                self.stepParameter.maxWidthContours = self.maxContoursWidth.getIntValue()
                self.stepParameter.minHeightContours = self.minContoursHeight.getIntValue()
                self.stepParameter.maxHeightContours = self.maxContoursHeight.getIntValue()
                self.stepParameter.minAspectRatio = self.minAspectRatio.getFloatValue()
                self.stepParameter.maxAspectRatio = self.maxAspectRatio.getFloatValue()
                self.stepParameter.contourNumThresh = self.numContourThresh.getIntValue()
            # erode and dilate
            elif self.stepParameter.stepAlgorithmName == MethodList.dilate.value or self.stepParameter.stepAlgorithmName == MethodList.erode.value:
                self.stepParameter.kernelSizeX = self.kernelSizeX.getIntValue()
                self.stepParameter.kernelSizeY = self.kernelSizeY.getIntValue()
                self.stepParameter.iterations = self.iterations.getIntValue()
            # Bit wise operations
            elif self.stepParameter.stepAlgorithmName == MethodList.bitwiseAnd.value \
                    or self.stepParameter.stepAlgorithmName == MethodList.bitwiseOr.value \
                    or self.stepParameter.stepAlgorithmName == MethodList.bitwiseNot.value \
                    or self.stepParameter.stepAlgorithmName == MethodList.bitwiseXor.value:

                self.stepParameter.resource2Index = self.sourceImage2.getPosValue() - 4
                self.stepParameter.maskIndex = self.maskImage.getPosValue() - 4
            # Adaptive thresh holding
            elif self.stepParameter.stepAlgorithmName == MethodList.adaptiveThreshold.value:
                self.stepParameter.maxThresholdValue = self.adaptiveThreshMaxVal.getIntValue()
                self.stepParameter.adaptiveMode = self.adaptiveMode.getValue()
                self.stepParameter.thresholdType1 = self.adaptiveThreshType.getValue()
                self.stepParameter.blockSize = self.adaptiveBlockSize.getIntValue()
                self.stepParameter.adaptiveC = self.adaptiveChangeVal.getIntValue()
            # Canny
            elif self.stepParameter.stepAlgorithmName == MethodList.canny.value:
                self.stepParameter.minThresh = self.cannyMinThresh.getIntValue()
                self.stepParameter.maxThresholdValue = self.cannyMaxThresh.getIntValue()
                self.stepParameter.canny_kernel_size = self.canny_kernel_size.getIntValue()
            # Rotate
            elif self.stepParameter.stepAlgorithmName == MethodList.rotate.value:
                self.stepParameter.rotateCode = self.rotateCode.getValue()
                self.stepParameter.rt_angle = self.rt_angle.getFloatValue()
                self.stepParameter.rt_center = (self.rt_centerX.getIntValue(), self.rt_centerY.getIntValue())
            # Flip
            elif self.stepParameter.stepAlgorithmName == MethodList.flip.value:
                self.stepParameter.flipCode = self.flipCode.getValue()
            # Original reference
            elif self.stepParameter.stepAlgorithmName == MethodList.originalReference.value:
                self.stepParameter.orRef1StepIdx = self.orRef1StepIdx.getPosValue()
                self.stepParameter.orRef2StepIdx = self.orRef2StepIdx.getPosValue()
                self.stepParameter.orRef3StepIdx = self.orRef3StepIdx.getPosValue()
                self.getReferenceLocation()
                # currentAlgorithm: Algorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()
                # currentAlgorithm.excuteStep(self.stepParameter.stepId - 1)

            # Hls range
            elif self.stepParameter.stepAlgorithmName == MethodList.hlsInRange.value:
                self.stepParameter.hlsLower = [self.hlsRangeFrame_HLower.getValue(),
                                               self.hlsRangeFrame_LLower.getValue(),
                                               self.hlsRangeFrame_SLower.getValue()]

                self.stepParameter.hlsUpper = [self.hlsRangeFrame_HUpper.getValue(),
                                               self.hlsRangeFrame_LUpper.getValue(),
                                               self.hlsRangeFrame_SUpper.getValue()]

                self.stepParameter.minRange = self.hls_min_range.getIntValue()
                self.stepParameter.maxRange = self.hls_max_range.getIntValue()

            # HSV range
            elif self.stepParameter.stepAlgorithmName == MethodList.hsvInRange.value:
                self.stepParameter.hsvLower = [self.hsvRangeFrame_HLower.getValue(),
                                               self.hsvRangeFrame_SLower.getValue(),
                                               self.hsvRangeFrame_VLower.getValue()]

                self.stepParameter.hsvUpper = [self.hsvRangeFrame_HUpper.getValue(),
                                               self.hsvRangeFrame_SUpper.getValue(),
                                               self.hsvRangeFrame_VUpper.getValue()]

                self.stepParameter.minRange = self.hsv_min_range.getIntValue()
                self.stepParameter.maxRange = self.hsv_max_range.getIntValue()
            # HSV + HLS range
            elif self.stepParameter.stepAlgorithmName == MethodList.hsv_hlsRange.value:
                self.stepParameter.hsvLower = [self.hsv_hlsRangeFrame_VHLower.getValue(),
                                               self.hsv_hlsRangeFrame_VSLower.getValue(),
                                               self.hsv_hlsRangeFrame_VVLower.getValue()]

                self.stepParameter.hsvUpper = [self.hsv_hlsRangeFrame_VHUpper.getValue(),
                                               self.hsv_hlsRangeFrame_VSUpper.getValue(),
                                               self.hsv_hlsRangeFrame_VVUpper.getValue()]

                self.stepParameter.hlsLower = [self.hsv_hlsRangeFrame_SHLower.getValue(),
                                               self.hsv_hlsRangeFrame_SLLower.getValue(),
                                               self.hsv_hlsRangeFrame_SSLower.getValue()]

                self.stepParameter.hlsUpper = [self.hsv_hlsRangeFrame_SHUpper.getValue(),
                                               self.hsv_hlsRangeFrame_SLUpper.getValue(),
                                               self.hsv_hlsRangeFrame_SSUpper.getValue()]
                self.stepParameter.minRange = self.hsv_hls_min_range.getIntValue()
                self.stepParameter.maxRange = self.hsv_hls_max_range.getIntValue()
            # BGR range
            elif self.stepParameter.stepAlgorithmName == MethodList.bgrInRange.value:
                self.stepParameter.bgrLower = [self.bgrRangeFrame_BLower.getValue(),
                                               self.bgrRangeFrame_GLower.getValue(),
                                               self.bgrRangeFrame_RLower.getValue()]

                self.stepParameter.bgrUpper = [self.bgrRangeFrame_BUpper.getValue(),
                                               self.bgrRangeFrame_GUpper.getValue(),
                                               self.bgrRangeFrame_RUpper.getValue()]

                self.stepParameter.minRange = self.bgr_min_range.getIntValue()
                self.stepParameter.maxRange = self.bgr_max_range.getIntValue()
            # BGR + HLS range
            elif self.stepParameter.stepAlgorithmName == MethodList.bgr_hlsRange.value:
                self.stepParameter.bgrLower = [self.bgr_hlsRangeFrame_BLower.getValue(),
                                               self.bgr_hlsRangeFrame_GLower.getValue(),
                                               self.bgr_hlsRangeFrame_RLower.getValue()]

                self.stepParameter.bgrUpper = [self.bgr_hlsRangeFrame_BUpper.getValue(),
                                               self.bgr_hlsRangeFrame_GUpper.getValue(),
                                               self.bgr_hlsRangeFrame_RUpper.getValue()]

                self.stepParameter.hlsLower = [self.bgr_hlsRangeFrame_HLower.getValue(),
                                               self.bgr_hlsRangeFrame_LLower.getValue(),
                                               self.bgr_hlsRangeFrame_SLower.getValue()]

                self.stepParameter.hlsUpper = [self.bgr_hlsRangeFrame_HUpper.getValue(),
                                               self.bgr_hlsRangeFrame_LUpper.getValue(),
                                               self.bgr_hlsRangeFrame_SUpper.getValue()]

                self.stepParameter.minRange = self.bgr_hls_min_range.getIntValue()
                self.stepParameter.maxRange = self.bgr_hls_max_range.getIntValue()
            # BGR + HSV range
            elif self.stepParameter.stepAlgorithmName == MethodList.bgr_hsvRange.value:
                self.stepParameter.bgrLower = [self.bgr_hsvRangeFrame_BLower.getValue(),
                                               self.bgr_hsvRangeFrame_GLower.getValue(),
                                               self.bgr_hsvRangeFrame_RLower.getValue()]

                self.stepParameter.bgrUpper = [self.bgr_hsvRangeFrame_BUpper.getValue(),
                                               self.bgr_hsvRangeFrame_GUpper.getValue(),
                                               self.bgr_hsvRangeFrame_RUpper.getValue()]

                self.stepParameter.hsvLower = [self.bgr_hsvRangeFrame_HLower.getValue(),
                                               self.bgr_hsvRangeFrame_SLower.getValue(),
                                               self.bgr_hsvRangeFrame_VLower.getValue()]

                self.stepParameter.hsvUpper = [self.bgr_hsvRangeFrame_HUpper.getValue(),
                                               self.bgr_hsvRangeFrame_SUpper.getValue(),
                                               self.bgr_hsvRangeFrame_VUpper.getValue()]

                self.stepParameter.minRange = self.bgr_hsv_min_range.getIntValue()
                self.stepParameter.maxRange = self.bgr_hsv_max_range.getIntValue()

            # Focus checking
            elif self.stepParameter.stepAlgorithmName == MethodList.focusChecking.value:
                self.stepParameter.threshFocus = self.focusThresh.getIntValue()

            # Hough lines
            elif self.stepParameter.stepAlgorithmName == MethodList.houghLines.value or \
                    self.stepParameter.stepAlgorithmName == MethodList.houghLinesP.value:
                self.stepParameter.hl_rho = self.hl_rho.getIntValue()
                self.stepParameter.hl_theta = self.hl_theta.getIntValue()
                self.stepParameter.hl_threshold = self.hl_threshold.getIntValue()
                self.stepParameter.hl_min_theta = self.hl_min_theta.getIntValue()
                self.stepParameter.hl_max_theta = self.hl_max_theta.getIntValue()
                self.stepParameter.hl_srn = self.hl_srn.getIntValue()
                self.stepParameter.hl_stn = self.hl_stn.getIntValue()
                self.stepParameter.hl_min_length = self.hl_min_length.getIntValue()
                self.stepParameter.hl_max_gap = self.hl_max_gap.getIntValue()
            # Background subtraction
            elif self.stepParameter.stepAlgorithmName == MethodList.subtractionKNN.value or \
                    self.stepParameter.stepAlgorithmName == MethodList.subtractionMog2.value:
                self.stepParameter.bs_history_frame_num = self.bs_historyNum.getIntValue()
                self.stepParameter.bs_dist2Threshold = self.bs_dist2Threshold.getFloatValue()
                self.stepParameter.bs_detect_shadow = self.bs_detectShadows.getValue()
                self.stepParameter.bs_process_image_index = self.bs_processImageIndex.getPosValue() - 4

            # translation image
            elif self.stepParameter.stepAlgorithmName == MethodList.translation.value:
                self.stepParameter.trans_move_x = self.trans_move_x.getIntValue()
                self.stepParameter.trans_move_y = self.trans_move_y.getIntValue()
            # reference translation
            elif self.stepParameter.stepAlgorithmName == MethodList.referenceTranslation.value:
                self.stepParameter.rt_baseSource = self.rt_baseSourceIndex.getValue()
                self.stepParameter.rt_destSource = self.rt_destSourceIndex.getValue()
                self.stepParameter.rt_type = self.rt_referenceType.getValue()
            # Draw circle
            elif self.stepParameter.stepAlgorithmName == MethodList.drawCircle.value:
                self.stepParameter.dc_center = (self.dc_centerX.getIntValue(), self.dc_centerY.getIntValue())
                self.stepParameter.dc_radius = self.dc_radius.getIntValue()
                self.stepParameter.dc_thickness = self.dc_thickness.getIntValue()
                self.stepParameter.dc_circleInput = self.dc_inputCircle.getValue()
            # Get Extreme
            elif self.stepParameter.stepAlgorithmName == MethodList.getExtreme.value:
                self.stepParameter.ge_extremeType = self.typeExtreme.getValue()
                self.stepParameter.ge_sourceContour = self.ge_contourInput.getValue()

            # Paint
            elif self.stepParameter.stepAlgorithmName == MethodList.paint.value:
                self.stepParameter.paintColor = (self.paintBlue.getValue(),
                                                 self.paintGreen.getValue(),
                                                 self.paintRed.getValue())

            # Min area rectangle
            elif self.stepParameter.stepAlgorithmName == MethodList.getMinAreaRect.value:
                self.stepParameter.mar_source_contours = self.mar_source_contour.getValue()

            # data matrix code 2 with get min area
            elif self.stepParameter.stepAlgorithmName == MethodList.dataMatrixReaderWithArea.value:
                self.stepParameter.get_min_area_box = self.get_min_area_box.getValue()

            # Find chessboard corners
            elif self.stepParameter.stepAlgorithmName == MethodList.findChessBoardCorners.value:
                self.stepParameter.cbc_sizeX = self.cbc_sizeX.getIntValue()
                self.stepParameter.cbc_sizeY = self.cbc_sizeY.getIntValue()

            # Resize
            elif self.stepParameter.stepAlgorithmName == MethodList.resize.value:
                self.stepParameter.rs_sizeX = self.rs_sizeX.getIntValue()
                self.stepParameter.rs_sizeY = self.rs_sizeY.getIntValue()
                self.stepParameter.rs_ratio = self.rs_ratio.getValue()
                self.stepParameter.rs_fX = self.rs_fX.getFloatValue()
                self.stepParameter.rs_fY = self.rs_fY.getFloatValue()

            # Connection Contours
            elif self.stepParameter.stepAlgorithmName == MethodList.connectionContour.value:
                self.stepParameter.cc_size = self.cc_size.getIntValue()
                self.stepParameter.cc_distance = self.cc_distance.getIntValue()
                self.stepParameter.cc_location = self.cc_location.getValue()

            # Split Channel
            elif self.stepParameter.stepAlgorithmName == MethodList.splitChannel.value:
                self.stepParameter.sc_channel_id = self.sc_channel_id.getIntValue()

            # Change Color
            elif self.stepParameter.stepAlgorithmName == MethodList.changeColor.value:
                self.stepParameter.change_color_code = self.change_color_code.getValue()
                self.stepParameter.change_color_mask = self.change_color_mask.getValue()

            # Threshold average
            elif self.stepParameter.stepAlgorithmName == MethodList.threshold_average.value:
                self.stepParameter.ta_brightness_reflection = self.ta_brightness_reflection.getIntValue()
            # Distance measurement
            elif self.stepParameter.stepAlgorithmName == MethodList.distance_point_to_point.value:
                self.stepParameter.p2p_point1 = self.p2p_point1_source.getValue()
                self.stepParameter.p2p_point2 = self.p2p_point2_source.getValue()
                self.stepParameter.p2p_range = self.p2p_range.getValue()

            elif self.stepParameter.stepAlgorithmName == MethodList.distance_point_to_line.value:
                self.stepParameter.p2l_point = self.p2l_point_source.getValue()
                self.stepParameter.p2l_point1_line = self.p2l_point1_line_source.getValue()
                self.stepParameter.p2l_point2_line = self.p2l_point2_line_source.getValue()
                self.stepParameter.p2l_range = self.p2l_range.getValue()
            # Angle measurement
            elif self.stepParameter.stepAlgorithmName == MethodList.angle_from_2_lines.value:
                self.stepParameter.af2l_point1_line1 = self.af2l_point1_line1.getValue()
                self.stepParameter.af2l_point2_line1 = self.af2l_point2_line1.getValue()
                self.stepParameter.af2l_point1_line2 = self.af2l_point1_line2.getValue()
                self.stepParameter.af2l_point2_line2 = self.af2l_point2_line2.getValue()
                self.stepParameter.af2l_valid_range = self.af2l_valid_range.getValue()
            # Tesseract
            elif self.stepParameter.stepAlgorithmName == MethodList.ocr_tesseract.value:
                self.stepParameter.ocr_tes_lange = self.available_language.getValue()

            # Deep learning for DDK
            elif self.stepParameter.stepAlgorithmName == MethodList.ddk_scratch_dl.value:
                self.stepParameter.dl_thresh = self.dl_thresh.getFloatValue()
                self.stepParameter.dl_resize_shape = (
                    self.dl_resizeWidth.getIntValue(), self.dl_resizeHeight.getIntValue())

            # Ignore area
            elif self.stepParameter.stepAlgorithmName == MethodList.ignore_areas.value:
                area_list = []
                for area_ignore in self.ignore_areas:
                    area_list.append(area_ignore.getValue())
                self.stepParameter.ignore_areas_list = area_list

            # Multi select area
            elif self.stepParameter.stepAlgorithmName == MethodList.multi_select_area.value:
                area_list = []
                for select_area in self.select_area_list:
                    area_list.append(select_area.getValue())
                self.stepParameter.select_areas_list = area_list
            # Change brightness
            elif self.stepParameter.stepAlgorithmName == MethodList.brightness_change.value:
                self.stepParameter.change_brightness_type = self.bright_change_type.getValue()
                self.stepParameter.change_brightness_value = self.brightness_change_value.getIntValue()
            # Histogram Equalization
            elif self.stepParameter.stepAlgorithmName == MethodList.histogram_equalization.value:
                self.stepParameter.he_type = self.his_equ_type.getValue()
                self.stepParameter.he_clipLimit = self.his_equ_clip_limit.getFloatValue()
                self.stepParameter.he_tile_grid_size = self.his_equ_grid_size.getIntValue()

            # Gama correction
            elif self.stepParameter.stepAlgorithmName == MethodList.gama_correction.value:
                self.stepParameter.gama_correction_value = self.gama_corrention_value.getFloatValue()
            # Reference Edge Corner
            elif self.stepParameter.stepAlgorithmName == MethodList.reference_edge_corner.value:
                self.stepParameter.rec_type = self.rec_type.getValue()
                self.stepParameter.rec_thresh_type = self.rec_thresh_type.getValue()
                self.stepParameter.rec_thresh = self.rec_thresh.getIntValue()
                self.stepParameter.rec_area = self.rec_area.getIntValue()
            elif self.stepParameter.stepAlgorithmName == MethodList.floodFill.value:
                self.stepParameter.flood_fill_seed_point = self.flood_fill_seed_point.getIntValue()
                self.stepParameter.flood_fill_color = self.flood_fill_color.getIntValue()
                self.stepParameter.flood_fill_lowdiff = self.flood_fill_lowdiff.getIntValue()
                self.stepParameter.flood_fill_updiff = self.flood_fill_updiff.getIntValue()
            # Viet OCR
            elif self.stepParameter.stepAlgorithmName == MethodList.viet_ocr.value:
                self.stepParameter.vo_model = self.vo_model.getValue()
                self.stepParameter.vo_device = self.vo_device.getValue()
                self.stepParameter.vo_weight_file_path = self.vo_weight_file.getValue()
                self.stepParameter.vo_vocab_path_file = self.vo_vocab_file.getValue()
            # contour linear regression
            elif self.stepParameter.stepAlgorithmName == MethodList.contour_linear_regression.value:
                self.stepParameter.clr_source_contour = self.clr_contour_source.getValue()
                self.stepParameter.clr_area_source = self.clr_area_source.getValue()
            # contours approximation
            elif self.stepParameter.stepAlgorithmName == MethodList.contourApproximation.value:
                self.stepParameter.c_apprx_source_contour = self.c_apprx_source_contour.getValue()
                self.stepParameter.c_apprx_epsilon_percent = self.c_apprx_epsilon_percent.getFloatValue()
                self.stepParameter.c_apprx_closed = self.c_apprx_closed.getValue()
            # contours fit line
            elif self.stepParameter.stepAlgorithmName == MethodList.fittingLine.value:
                self.stepParameter.cfl_source_contour = self.cfl_source_contour.getValue()
                self.stepParameter.cfl_distance_type = self.cfl_distance_type.getValue()
                self.stepParameter.cfl_param = self.cfl_param.getFloatValue()
                self.stepParameter.cfl_reps = self.cfl_reps.getFloatValue()
                self.stepParameter.cfl_aeps = self.cfl_aeps.getFloatValue()

            # segmentation yolo v8
            elif self.stepParameter.stepAlgorithmName == MethodList.segment_yolov8.value:
                self.stepParameter.path_weight_yolov8 = self.path_weight_yolov8.getValue()
                self.stepParameter.confidence_yolov8 = self.confidence_yolov8.getFloatValue()

            # Multi select area 2
            elif self.stepParameter.stepAlgorithmName == MethodList.auto_multi_circle.value:
                self.stepParameter.amc_circle_list = self.amc_circle_list.getValue()
                self.stepParameter.amc_circle_radius_1 = self.amc_radius_1.getFloatValue()
                self.stepParameter.amc_circle_radius_2 = self.amc_radius_2.getFloatValue()

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Step Setting: {}".format(error))
            messagebox.showerror("Step Setting", "{}".format(error))
            return False
        return True

    def getReferenceLocation(self):
        ret, resultList, text = self.mainWindow.researchingTab.currentAlgorithm.executeStep(
            self.stepParameter.stepId - 1)
        refPointArea1 = []
        refPointArea2 = []
        refPointArea3 = []
        for result in resultList:
            if result.stepId == self.stepParameter.orRef1StepIdx:
                refPointArea1 = result.detectAreaList
            elif result.stepId == self.stepParameter.orRef2StepIdx:
                refPointArea2 = result.detectAreaList
            elif result.stepId == self.stepParameter.orRef3StepIdx:
                refPointArea3 = result.detectAreaList

        if len(refPointArea1) < 1:
            messagebox.showerror("Cannot find reference position 1")
            return
        if len(refPointArea2) < 1:
            messagebox.showerror("Cannot find reference position 2")
            return
        if len(refPointArea3) < 1:
            messagebox.showerror("Cannot find reference position 3")
            return

        self.stepParameter.originalRefPoint1 = (int((refPointArea1[0][0] + refPointArea1[0][2]) / 2),
                                                int((refPointArea1[0][1] + refPointArea1[0][3]) / 2))

        self.stepParameter.originalRefPoint2 = (int((refPointArea2[0][0] + refPointArea2[0][2]) / 2),
                                                int((refPointArea2[0][1] + refPointArea2[0][3]) / 2))

        self.stepParameter.originalRefPoint3 = (int((refPointArea3[0][0] + refPointArea3[0][2]) / 2),
                                                int((refPointArea3[0][1] + refPointArea3[0][3]) / 2))

    def clickBtnExit(self):
        self.okFlag = False
        self.masterWin.settingStepDone()
