from ImageProcess.Algorithm.MethodList import MethodList
import enum
class AlgorithmResultKey(enum.Enum):
    stepId = "stepId"
    methodName = "method_name"
    circleList = "circle_list"
    circle = "circle"
    basePoint = "basePoint"
    workingArea = "working_area"
    detectAreaList = "detect_area_list"
    passed = "passed"
    contourList = "contour_list"
    value = "value"
    valueList = "value_list"
    drawImage = "draw_image"
    pointList = "point_list"
    point = "point"
    line = "line"
    lineList = "line_list"
    extreme = "extreme"
    angle = "angle"
    box = "box"
    boxList = "box_list"
    barcodeList = "barcode_list"
    rotationList = "rotation_list"
    rotation = "rotation"
    distance = "distance"
    text = "text"
    ignore_area_list = "ignore_area_list"
    class_names = "class_names"
    list_center_min_rec = "list_center_min_rec"

class AlgorithmResult:
    stepId = None
    methodName: MethodList
    circleList = None
    circle = None
    workingArea = [0, 0, 0, 0] #(startX, StartY, endX, endY)
    basePoint = None #(startX, StartY)
    detectAreaList = [] #(startX, StartY, endX, endY)
    passed = False
    contourList = []
    value = None
    valueList = None
    point = None
    pointList = None
    line = None
    lineList = None
    extreme = None
    angle = None
    box = None
    boxList = None
    barcodeList = None
    rotationList = None
    rotation = None
    distance = None
    ignore_area_list = None
    text = None
    class_names = None
    list_center_min_rec = None

    def __init__(self, workingArea=None, detectAreaList=None, stepId = 0, passed=False,
                 drawImage=None, contourList = None, circle=None, circleList=None, point=None, pointList=None,
                 line=None, lineList=None, basePoint=None, extreme=None, angle=None,
                 methodName = None, value=None, valueList=None, box=None, boxList=None, barcodeList=None,
                 rotationList=None, rotation=None, text=None, ignore_area_list = None, class_names=None,
                 distance=None, list_center_min_rec=None):
        self.drawImage = drawImage
        self.workingArea = workingArea
        self.detectAreaList = detectAreaList if detectAreaList is not None else []
        self.passed = passed
        self.circleList = circleList
        self.contourList = contourList
        self.methodName = methodName
        self.stepId = stepId
        self.value = value
        self.valueList = valueList
        self.point = point
        self.pointList = pointList
        self.circle = circle
        self.line = line
        self.basePoint = basePoint
        self.lineList = lineList
        self.extreme = extreme
        self.angle = angle
        self.box = box
        self.boxList = boxList
        self.barcodeList = barcodeList
        self.rotationList = rotationList
        self.rotation = rotation
        self.distance = distance
        self.text = text
        self.ignore_area_list = ignore_area_list
        self.class_names = class_names
        self.list_center_min_rec = list_center_min_rec

    def getValue(self, key):
        if key is None:
            return None
        elif key == AlgorithmResultKey.stepId.value:
            return self.stepId
        elif key == AlgorithmResultKey.methodName.value:
            return self.methodName
        elif key == AlgorithmResultKey.circleList.value:
            return self.circleList
        elif key == AlgorithmResultKey.passed.value:
            return self.passed
        elif key == AlgorithmResultKey.basePoint.value:
            return self.basePoint
        elif key == AlgorithmResultKey.workingArea.value:
            return self.workingArea
        elif key == AlgorithmResultKey.detectAreaList.value:
            return self.detectAreaList
        elif key == AlgorithmResultKey.contourList.value:
            return self.contourList
        elif key == AlgorithmResultKey.value.value:
            if self.value is None and self.valueList is not None:
                self.value = self.valueList[0]
            return self.value
        elif key == AlgorithmResultKey.valueList.value:
            return self.valueList
        elif key == AlgorithmResultKey.drawImage.value:
            return self.drawImage
        elif key == AlgorithmResultKey.circle.value:
            if self.circle is None and self.circleList is not None:
                self.circle = self.circleList[0]
            return self.circle
        elif key == AlgorithmResultKey.circleList.value:
            return self.circleList
        elif key == AlgorithmResultKey.point.value:
            if self.point is None and self.pointList is not None:
                self.point = self.pointList[0]
            return self.point
        elif key == AlgorithmResultKey.pointList.value:
            return self.pointList
        elif key == AlgorithmResultKey.line.value:
            if self.line is None and self.lineList is not None:
                self.line = self.lineList[0]
            return self.line
        elif key == AlgorithmResultKey.lineList.value:
            return self.lineList
        elif key== AlgorithmResultKey.extreme:
            return self.extreme
        elif key == AlgorithmResultKey.angle.value:
            return self.angle
        elif key == AlgorithmResultKey.box.value:
            if self.box is None and self.boxList is not None:
                self.box = self.boxList[0]
            return self.box
        elif key == AlgorithmResultKey.boxList.value:
            return self.boxList
        elif key == AlgorithmResultKey.barcodeList.value:
            return self.barcodeList
        elif key == AlgorithmResultKey.rotation.value:
            if self.rotation is None and self.rotationList is not None:
                self.rotation = self.rotationList[0]
            return self.rotation
        elif key == AlgorithmResultKey.rotationList.value:
            return self.rotationList
        elif key == AlgorithmResultKey.distance.value:
            return self.distance
        elif key == AlgorithmResultKey.text.value:
            return self.text
        elif key == AlgorithmResultKey.ignore_area_list.value:
            return self.ignore_area_list
        elif key == AlgorithmResultKey.class_names.value:
            return self.class_names
        elif key == AlgorithmResultKey.list_center_min_rec.value:
            return self.list_center_min_rec
        else:
            return None
