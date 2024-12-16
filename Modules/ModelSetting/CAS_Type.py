import enum

class CAS_Type(enum.Enum):

    robot_x_pos_y_pos = "x = x and y = y"
    robot_x_y_exchanged = "x=y and y = x"
    robot_x_inv_y_pos = "x = -x and y =y"
    robot_x_y_exchanged_y_inv = "x = -y, y = x"