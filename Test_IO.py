from IO_Rasp import *
import cv2 as cv
from CommonAssit import TimeControl

if __name__ == '__main__':
    take_pic_btn = Input_Port(4) # cổng input
    ok_output = Output_Port(5) # cổng đầu ra OK
    ok_output.off()
    ng_output = Output_Port(6) # Cổng đầu ra NG
    ng_output.off()
    valid_press_time = 500 # thời gian xác nhận nút bấm đã bấm để lọc nhiễu
    release_time = TimeControl.time()
    in_pressing = False
    while True:
        if take_pic_btn.is_pressed():
            if TimeControl.time() - release_time > valid_press_time:
                # Trong khi phát hiện nút bấm đủ thời gian thì xác nhận là đã nhận tín hiệu chụp ảnh
                if not in_pressing:
                    print("press")
                in_pressing = True
        else:
            in_pressing = False
            release_time = TimeControl.time()

        wk = cv.waitKey(3) # nhập key input từ bàn phím
        if wk == ord("o"): # nếu nhập "o" Thì on ouput đầu ra OK lên 3 giây
            ok_output.on_with_time(3000)
        if wk == ord("n"): # nếu nhập "n" Thì on ouput đầu ra NG lên 3 giây
            ok_output.on_with_time(3000)
        if wk == ord("q"): # nếu nhập "q" thì thoát chương trình
            break
