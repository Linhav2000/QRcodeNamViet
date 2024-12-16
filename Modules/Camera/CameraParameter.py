
import enum
from Modules.Camera.CameraNameList import CameraNameList

class CameraInterface(enum.Enum):
    usb3InterFace = "USB 3"
    gigEInterFace = "GigE"

class CameraBrand(enum.Enum):
    basler = "Basler"
    csr = "CSR"
    wc_dshow = "WC+DSHOW"
    wc_default = "WC+Default"

    ipCamera = "Ip camera"
    pointGrey = "Point Grey"
    hikVision = "Hik Vision"
    imageSource = "Imaging Source"


class CameraFlip(enum.Enum):
    none = "None"
    vertically = "Vertically"
    horizontally = "Horizontally"
    both = "Both"

class CameraRotate(enum.Enum):
    _zero = "0"
    _90ClockWise = "90ClockWise"
    _90CounterClockWise = "90CounterClockWise"
    _180degrees = "180"


class CameraParameter:
    name = CameraNameList.camera_0.value
    id = 0
    interface = CameraInterface.usb3InterFace.value
    brand = CameraBrand.wc_default.value
    flip = CameraFlip.none.value
    rotate = CameraRotate._zero.value
    textScale = 1.0
    textThickness = 3
    feature_path = ""
    status = False

    def makeStandard(self):
        self.id = int(self.id)