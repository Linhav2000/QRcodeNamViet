import enum
import cv2 as cv
from ImageProcess.Algorithm.MethodList import MethodList
from ImageProcess.Algorithm.AlgorithmResult import AlgorithmResultKey

class ImageRotate(enum.Enum):
    none = -1
    lock_wise_90 = cv.ROTATE_90_CLOCKWISE
    counter_lock_wise_90 = cv.ROTATE_90_COUNTERCLOCKWISE
    rotate_180 = cv.ROTATE_180

class ImageFlip(enum.Enum):
    none = 2
    vertical = 0
    horizontal = 1
    both = -1

class DistanceType(enum.Enum):
    DIST_USER = cv.DIST_USER
    DIST_L1 = cv.DIST_L1
    DIST_L2 = cv.DIST_L2
    DIST_C = cv.DIST_C
    DIST_L12 = cv.DIST_L12
    DIST_FAIR = cv.DIST_FAIR
    DIST_WELSCH = cv.DIST_WELSCH
    DIST_HUBER = cv.DIST_HUBER

class ThresholdCode(enum.Enum):
    _None = -1
    Binary = cv.THRESH_BINARY
    Binary_Invoke = cv.THRESH_BINARY_INV
    Trunc = cv.THRESH_TRUNC
    ToZero = cv.THRESH_TOZERO
    ToZero_Invoke = cv.THRESH_TOZERO_INV
    Otsu = cv.THRESH_OTSU
    Triangle = cv.THRESH_TRIANGLE
    Mask = cv.THRESH_MASK

class AdaptiveThreshMode(enum.Enum):
    Gaussian_C = cv.ADAPTIVE_THRESH_GAUSSIAN_C
    Mean_C = cv.ADAPTIVE_THRESH_MEAN_C

class RF_Type(enum.Enum):
    top = "Top"
    bottom = "Bottom"
    left = "Left"
    right = "Right"
    all = "All"

class ReferenceEdgeCornerType(enum.Enum):
    top = "Top"
    right = "Right"
    bottom = "Bottom"
    left = "Left"
    left_top = "Left Top"
    top_right = "Top Right"
    right_bottom = "Right Bottom"
    bottom_left = "Bottom Left"

class CvtColorCode(enum.Enum):
    bgr2Gray = cv.COLOR_BGR2GRAY
    gray2Bgr = cv.COLOR_GRAY2BGR
    bgr2Rgb = cv.COLOR_BGR2RGB
    rgb2Bgr = cv.COLOR_RGB2BGR
    rgb2Gray = cv.COLOR_RGB2GRAY
    gray2Rgb = cv.COLOR_GRAY2RGB
    bgr2Hsv = cv.COLOR_BGR2HSV
    hsv2Bgr = cv.COLOR_HSV2BGR
    rgb2Hsv = cv.COLOR_RGB2HSV
    hsv2Rgb = cv.COLOR_HSV2RGB
    bgr2Hls = cv.COLOR_BGR2HLS
    hls2Bgr = cv.COLOR_HLS2BGR
    rgb2Hls = cv.COLOR_RGB2HLS
    hls2Rgb = cv.COLOR_HLS2RGB

class ChangeColorCode(enum.Enum):
    black2white = "Black to white"
    white2black = "White to black"
    black2average = "Black to average"
    white2average = "White to average"

class SourceImageName(enum.Enum):
    sourceImage = "sourceImage"
    bs_processImage = "bs_process"
    rt_baseSource = "rt_baseSource"
    rt_currentSource = "rt_currentSource"
    sourceImage2 = "sourceImage2"
    mask = "mask"

class StepParameter:
    stepAlgorithmName = MethodList.colorDetect.value
    activeFlag = False
    resourceIndex = (-1, AlgorithmResultKey.drawImage.value)
    resource2Index = -1
    maskIndex = -1
    stepId = 0
    workingArea = None #(startX, StartY, endX, endY)
    templateName = "template"
    refImageName = "refImage"
    minMatchingValue = 0.5
    multiMatchingFlag = False
    threshold = 0.6
    threshold_thresh_val = 100
    minThresh = 50
    maxThresholdValue = 255
    canny_kernel_size = 3
    thresholdType1 = ThresholdCode.Binary.value
    thresholdType2 = ThresholdCode._None.value
    adaptiveMode = AdaptiveThreshMode.Mean_C.value
    blockSize = 3
    adaptiveC = 1
    blurSize = 3
    blurSigmaX = 0
    cvtColorCode = CvtColorCode.bgr2Gray.value
    averageColor = [0, 0, 0]
    bgrToleranceRange = [10, 10, 10]

    # range color
    bgrLower = [0, 0, 0]
    bgrUpper = [255, 255, 255]

    hsvLower = [0, 0, 0]
    hsvUpper = [255, 255, 255]

    hlsLower = [0, 0, 0]
    hlsUpper = [255, 255, 255]


    minRange = 0
    maxRange = 100

    # Hough circle
    nonzeroThresh = 100
    nonzero_range = (0, 1)
    houghCircleMinDist = 10
    houghCircleParm1 = 50
    houghCircleParm2 = 60
    houghCircleMinRadius = 50
    houghCircleMaxRadius = 60
    houghCircleBetweenDist = 100
    houghCircleTrustNumber = 1


    threshFocus = 100

    # contour
    minAreaContours = -1
    maxAreaContours = -1
    minWidthContours = -1
    maxWidthContours = -1
    minHeightContours = -1
    maxHeightContours = -1
    minAspectRatio = -1
    maxAspectRatio = -1
    fillColor = (255, 255, 255)
    contourNumThresh = 0
    contours_binary_source = (-2, AlgorithmResultKey.drawImage.value)
    contours_area_source = (-2, AlgorithmResultKey.workingArea.value)

    #blur
    kernelSizeX = 3
    kernelSizeY = 3
    iterations = 1

    # flip and rotate
    rotateCode = ImageRotate.none.value
    flipCode = ImageFlip.none.value
    rt_angle = 0
    rt_center = (-1, -1)

    # original reference
    orRef1StepIdx = 0
    orRef2StepIdx = 1
    orRef3StepIdx = 2

    originalRefPoint1 = None
    originalRefPoint2 = None
    originalRefPoint3 = None

    # Hough lines
    hl_rho = 1
    hl_theta = 1
    hl_threshold = 150
    hl_srn = 0
    hl_stn = 0
    hl_min_theta = 0
    hl_max_theta = 180
    hl_min_length = 100
    hl_max_gap = 10


    # background subtraction
    bs_history_frame_num = 1
    bs_dist2Threshold = 400.0
    bs_detect_shadow = True
    bs_process_image_index = -1
    bs_processWorkingArea = None #(startX, StartY, endX, endY)

    # translation
    trans_move_x = 0
    trans_move_y = 0

    # reference translation
    rt_baseSource = (-2, AlgorithmResultKey.point)
    rt_baseWorkingArea = None #(startX, StartY, endX, endY)
    rt_destSource = (-2, AlgorithmResultKey.point)
    rt_currentWorkingArea = None #(startX, StartY, endX, endY)
    rt_type = RF_Type.left.value

    # draw circle
    dc_center = [0, 0]
    dc_radius = 1
    dc_thickness = 1
    dc_circleInput = (-2, AlgorithmResultKey.circle.value)

    # Get Extreme
    ge_sourceContour = (-2, AlgorithmResultKey.contourList.value)
    ge_extremeType = RF_Type.all.value

    # paint
    paintColor = (255, 255, 255)
    paintArea = None

    # min area rectangle
    mar_source_contours = (-2, AlgorithmResultKey.contourList.value)

    # data matrix code 2 with get min area
    get_min_area_box = (-2, AlgorithmResultKey.boxList.value)

    # find chess board corners
    cbc_sizeX = 1
    cbc_sizeY = 1

    # Resize
    rs_sizeX = 1
    rs_sizeY = 1
    rs_ratio = False
    rs_fX = 1
    rs_fY = 1

    # Connection Contours
    cc_size = 1
    cc_distance = 1
    cc_location = -1

    # Split channel
    sc_channel_id = 0

    # Change color
    change_color_code = ChangeColorCode.black2average.value
    change_color_mask = (-2, AlgorithmResultKey.drawImage.value)

    # threshold average
    ta_brightness_reflection = 0

    # distance measurement
    p2p_point1 = (-2, AlgorithmResultKey.point.value)
    p2p_point2 = (-2, AlgorithmResultKey.point.value)
    p2p_range = (0, 1)

    p2l_point = (-2, AlgorithmResultKey.point.value)
    p2l_point1_line = (-2, AlgorithmResultKey.point.value)
    p2l_point2_line = (-2, AlgorithmResultKey.point.value)
    p2l_range = (0, 1)

    # angle measurement
    af2l_point1_line1 = (-2, AlgorithmResultKey.point.value)
    af2l_point2_line1 = (-2, AlgorithmResultKey.point.value)
    af2l_point1_line2 = (-2, AlgorithmResultKey.point.value)
    af2l_point2_line2 = (-2, AlgorithmResultKey.point.value)
    af2l_valid_range = (0, 1)

    # OCR Tesseract
    ocr_tes_lange = ""

    # Deep learning thresh
    dl_thresh = 0.5
    dl_resize_shape = (-1, -1)

    # ignore areas
    ignore_areas_list = []

    # select areas
    select_areas_list = []

    def makeStandard(self):
        self.multiMatchingFlag = bool(self.multiMatchingFlag)

    # roate image with angle
    riwa_angle = 0
    riwa_reshape = True
    riwa_center = None

    # change brightness
    change_brightness_type = "Lighter"
    change_brightness_value = 0

    # histogram equalization
    he_type = "Normal Equalization"
    he_clipLimit = 2.0
    he_tile_grid_size = 8

    # gama correction
    gama_correction_value = 1.0

    # reference adge corner
    rec_type = "Top"
    rec_thresh_type = ThresholdCode.Binary_Invoke.value
    rec_thresh = 100
    rec_area = 100
    rec_origin_extreme = (0, 1, 2, 3)

    # flood fill
    flood_fill_seed_point = (0, 0)
    flood_fill_color = 255
    flood_fill_lowdiff = 0
    flood_fill_updiff = 0

    # Viet OCR
    vo_model = "vgg_transformer"
    vo_device = "cpu"
    vo_weight_file_path = ""
    vo_vocab_path_file = ""

    # contour linear regression
    clr_source_contour = (-2, AlgorithmResultKey.contourList.value)
    clr_area_source = (-2, AlgorithmResultKey.workingArea.value)

    # contours approximation
    c_apprx_epsilon_percent = 0.01
    c_apprx_closed = True
    c_apprx_source_contour = (-2, AlgorithmResultKey.contourList.value)

    # contours fit line
    cfl_source_contour = (-2, AlgorithmResultKey.contourList.value)
    cfl_distance_type = DistanceType.DIST_L2.value
    cfl_param = 0
    cfl_reps = 0.01
    cfl_aeps = 0.01

    """segmentation yolo v8"""
    path_weight_yolov8 = ""
    confidence_yolov8 = 0.5

    """auto multi circle"""   # cải tiến multi select area
    amc_circle_list = (-2, AlgorithmResultKey.circleList.value)
    amc_circle_radius_1 = 0
    amc_circle_radius_2 = 0
