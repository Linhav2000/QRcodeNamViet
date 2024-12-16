from Modules.ModelSetting.CAS_Type import CAS_Type
from Modules.Camera.CameraParameter import CameraRotate
class AS_Parameter:
    name = ""
    as_type = ""
    casType = CAS_Type.robot_x_pos_y_pos.value
    robot_pixel_mm_Scale = 1
    robot_mm_moving_Scale = 1
    delayTakepicTime = 200
    exceptDelta = 10
    robotOffset = (0, 0)
    rotate = CameraRotate._zero.value
    preProcess_algorithm = ""

    image_point_1 = (0, 0)
    image_point_2 = (10, 15)
    image_point_3 = (5, 60)

    robot_point_1 = (1, 5)
    robot_point_2 = (20, 30)
    robot_point_3 = (8, 55)
    getPointsAlgorithm = ""

    transform_matrix = []
