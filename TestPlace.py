# import cv2 as cv
# from CommonAssit import TimeControl
# # captureVideo = cv.VideoCapture("D:\\Duc\\Document\\Project\\Noone\\Gan_tren_banh.mp4")
# #
# # while captureVideo.isOpened():
# #     ret, image = captureVideo.read()
# #     if ret:
# #         image = cv.resize(image, dsize=(800, 600))
# #         cv.imshow("Image", image)
# #         cv.imwrite(f"./Save_image/{TimeControl.time()}.jpg", image)
# #         cv.waitKey(50)
# #
# # cv.destroyAllWindows()
# #
# import glob
#
# imagePaths = glob.glob(r"D:\Vision\tensorflow1\models\research\object_detection\images\train\*.jpg",recursive=True)
#
# for imagePath in imagePaths:
#     image = cv.imread(imagePath)
#     image = cv.resize(image, dsize=(800, 1300))
#     cv.imwrite(rf"D:\Vision\tensorflow1\models\research\object_detection\images\Resize\{int(TimeControl.time())}.jpg", image)
#     print(TimeControl.time())
#     TimeControl.sleep(3)
#

# cv.destroyAllWindows()
# Change brightness
# import glob
#
# imagePaths = glob.glob(r"D:\Duc\Document\Project\TSB\DDK\DDK Check\Teaching_image\Train_image_2021_10_25\cut_2021_10_25\*.png",recursive=True)
#
# for imagePath in imagePaths:
#     image = cv.imread(imagePath)
#     image = cv.resize(image, dsize=None, fx=0.6, fy=0.6)
#     cv.imwrite(rf"D:\Duc\Document\Project\TSB\DDK\DDK Check\Teaching_image\Train_image_2021_10_25\resize_2021_10_25\{int(TimeControl.time())}.jpg", image)
#     print(TimeControl.time())
#     TimeControl.sleep(3)


# from sklearn import  svm
# svc = svm.SVC()
#
# import glob
# from ImageProcess import ImageProcess
#
# imagePaths = glob.glob(r"D:\Duc\Code\SVM_Onclass_Study\Train_Data\*.png",recursive=True)
#
# for imagePath in imagePaths:
#     image = cv.imread(imagePath)
#     image = cv.resize(image, dsize=(500, 500))
#     # image = ImageProcess.processRotateImage(image, cv.ROTATE_90_CLOCKWISE)
#     cv.imwrite(rf"D:\Duc\Code\SVM_Onclass_Study\Train_Data\resize\{int(TimeControl.time())}.jpg", image)
#     print(TimeControl.time())
#     TimeControl.sleep(3)

# from CommonAssit import TimeControl
# import pyautogui
# from pynput.keyboard import Key, Controller
#
# if __name__ == '__main__':
#     time = TimeControl.time()
#     while True:
#         pyautogui.click(500, 500)
#
#         keyboard = Controller()
#
#         keyboard.press(Key.enter)
#         keyboard.release(Key.enter)
#
#         TimeControl.sleep(600000)
#
#

# from ImageProcess import ImageProcess
# image = cv.imread("Save_image/1620741450091.5425.bmp")
#
# img = cv.resize(image, dsize=(800, 600))
# img = ImageProcess.processCvtColor(img, cv.COLOR_RGB2GRAY)
#
# wheel_area = (396, 85, 27, 83)
# check_area = (380, 194, 45, 31)
#
# wheel_image = img[wheel_area[1]: (wheel_area[1] + wheel_area[3]), wheel_area[0]: (wheel_area[0] + wheel_area[2])]
# check_image = img[check_area[1]: (check_area[1] + check_area[3]), check_area[0]: (check_area[0] + check_area[2])]
#
#
# import numpy as np
#
#
# norm = np.linalg.norm
#
# def distance_point_to_line(point=(0, 0), line=((0, 0), (1, 1))):
#     try:
#         point_line1 = np.array(line[0])
#         point_line2 = np.array(line[1])
#
#         single_point = np.array(point)
#
#         d = np.abs(norm(np.cross(point_line2 - point_line1, point_line1 - single_point))) / norm(point_line2 - point_line1)
#         return True, d
#     except Exception as error:
#         print(f"{error}")
#         return False, 0
#
# point = (5, 6)
# line = ((1, 1), (2, 1))
#
# print(distance_point_to_line(point, line))
#
# import tkinter as tk
# from View.Common.RangeSlider import RangeSlider
#
# root = tk.Tk()
# scale = tk.Scale(root, from_=0, to=100, showvalue=0)
# scale.pack()
# scale.set(50)
# #
# # slider = RangeSlider(root, width = 400, height = 60, min_val = -100, max_val = 100, init_lis = [-50, 75], show_value = True)
# # slider.getValues()
# # slider.pack()
# # root.title("Slider Widget")
# # slider.setValue([-20, 50])
# root.mainloop()

# print(slider.getValues())

#
# import pytesseract
# import cv2 as cv
# from CommonAssit import TimeControl
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# imagePath=r'D:\Duc\Code\OCR\train\eng.arial.exp0.png'
# image = cv.imread(imagePath)
#
# time = TimeControl.time()
# text = pytesseract.image_to_string(image, lang = 'eng2')
# print(TimeControl.time() - time)
# print(text)
#
# print(pytesseract.get_languages(config=''))

# import matplotlib.pyplot as plt

# from sklearn import datasets
# from sklearn import svm
#
# digits = datasets.load_digits()
# print(digits.data)
# print(digits.target)
# print(digits.images[0])

# import os
# file_name = r"D:\Duc\Code\OCR\train\eng.arial.exp0.png"
# print(os.path.dirname(file_name))


# from pypylon import pylon
# from pypylon import genicam
# import numpy
#
# baslerGigECamera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
# baslerGigECamera.Open()
# print("DeviceClass: ", baslerGigECamera.GetDeviceInfo().GetDeviceClass())
# print("DeviceFactory: ", baslerGigECamera.GetDeviceInfo().GetDeviceFactory())
# print("ModelName: ", baslerGigECamera.GetDeviceInfo().GetModelName())
#
# # baslerGigECamera.RegisterConfiguration(pylon.ConfigurationEventHandler(), pylon.RegistrationMode_ReplaceAll,
# #                                             pylon.Cleanup_Delete)
#
# # baslerGigECamera.TriggerMode.SetValue('On')
# baslerGigECamera.LineSelector.SetValue('Line2')
# baslerGigECamera.LineMode.SetValue('Output')
# baslerGigECamera.LineSource.SetValue('UserOutput1')
# baslerGigECamera.UserOutputSelector.SetValue('UserOutput1')
# line3_value = baslerGigECamera.UserOutputValue.GetValue()
# baslerGigECamera.UserOutputValue.SetValue(False)
# print(line3_value)
# baslerGigECamera.Close()
#
# import cv2 as cv
# import numpy
# from CommonAssit import TimeControl
# from ImageProcess import ImageProcess
#
# image = cv.imread(r"D:\Duc\Code\Vision\dist\save_images\Station_1\block break 1\000005.png")
# time = TimeControl.time()
# averageColor = image.mean(axis=0).mean(axis=0)
# print(TimeControl.time() - time)
# print(averageColor)
# time = TimeControl.time()
# avg_color_per_row = numpy.average(image, axis=0)
# avg_color = numpy.average(avg_color_per_row, axis=0)
# print(TimeControl.time() - time)
# print(avg_color)
#
# time = TimeControl.time()
# averageColor = cv.mean(image)
# print(TimeControl.time() - time)
# print(averageColor)

# cv.imshow("image original", image)
#
# image_rotate = ImageProcess.rotateImageWithAngle(image, 20)
#
# cv.imshow("image rotate", image_rotate)
# cv.imwrite(r"D:\Duc\Document\Project\TSB\FPCB_Inspection\picture\robot_points.png", image_rotate)
#
# cv.waitKey(0)
#
# cv.destroyAllWindows()

# from CommonAssit import PathFileControl
# import os
# path = r"./data/sdgg/sfgsdfg/gsdfgdsg"
# if not PathFileControl.pathExisted(path):
#     os.makedirs(path, exist_ok=False)
# print("The new directory is created!")

# import glob
# from CommonAssit.FileManager import *
# from tkinter import *
# image_name = glob.glob(r'D:\Duc\Document\Others\wedding_pic\Da_chon\*.JPG')
# image_name = [name.split("\\")[-1] + ", " for name in image_name]
# textFile = TextFile(r"D:\Duc\Document\Others\wedding_pic\duc_tham_edit.txt")
# textFile.dataList = [image_name]
# textFile.saveFile()
# print(image_name)
#
# image_names = ['7M6A0020', '7M6A0026', '7M6A0062', '7M6A0113', '7M6A0150', '7M6A0188', '7M6A0233', '7M6A0308', '7M6A0344', '7M6A0668', '7M6A0795']
#
#
# for image_name in image_names:
#     try:
#         image_path = rf"D:\Duc\Document\Others\wedding_pic\101EOS5D 1\7M6A0020.JPG"
#         image = cv.imread(image_path)
#         cv.imwrite(rf"D:\Duc\Document\Others\wedding_pic\anh de ban\{image_name}.JPG", image)
#         cv.imshow("image", image)
#         cv.waitKey(10)
#     except Exception as error:
#         print(image_name)
#
# cv.destroyAllWindows()

# from  CommonAssit import TimeControl
# import numpy as np
#
# image_path = rf"D:\Duc\Document\Others\wedding_pic\101EOS5D 1\7M6A0020.JPG"
#
# time = TimeControl.time()
#
# image = cv.imread(image_path)
#
# print(f"CV read time = {TimeControl.time() - time}")
#
# time = TimeControl.time()
#
# image = cv.imdecode(np.fromfile(image_path, dtype=np.uint8), cv.IMREAD_COLOR)
#
# print(f"np read time = {TimeControl.time() - time}")
# import numpy as np
# from matplotlib import pyplot as plt
# from CommonAssit import TimeControl
# import tkinter
# size = 0.3
# vals = np.array([[60.], [37.], [29.]])
# cmap = plt.get_cmap("tab20c")
# outer_colors = cmap(np.arange(3)*4)
# inner_colors = cmap(np.array([1, 2, 5, 6, 9, 10]))
# plt.figure(figsize=(10,10))
# plt.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
#        wedgeprops=dict(width=size, edgecolor='w'))
#
# plt.show()

# print(hex(int(format(ord("@"), "x")) + int(format(ord("F"), "x"))))
# from CommonAssit.FileManager import *
# from CommonAssit import TimeControl
# def getDictFromCSV():
#     lang_dict = {}
#     csvFile = CsvFile("./resource/Languages/Multi_Language.csv")
#     data_list = csvFile.readFile()
#     lang_list = []
#     for i in range(1, len(data_list[1])):
#         lang_dict[data_list[1][i]] = {}
#         lang_list.append(data_list[1][i])
#
#     for i in range(2, len(data_list)):
#         for j, lang in enumerate(lang_list):
#             lang_dict[lang][data_list[i][0]] = data_list[i][j+1]
#     print(lang_dict)
#
# getDictFromCSV()
# TimeControl.sleep(100)
# from CommonAssit import TimeControl
# import os
# import os
# time = TimeControl.time()
# dir_name = r"D:\Duc\Document\Project\TSB\FPCB_Inspection\picture\Ảnh đợt 4 20211222\GLassed_HighLight\o_scratch"
# _, _, image_paths = next(os.walk(dir_name), (None, None, []))
# full_paths = [os.path.join(dir_name, image_path) for image_path in image_paths]
# print(TimeControl.time() - time)
#
# TimeControl.sleep(5)
'''
import numpy as np
import cv2 as cv
import skimage.io as io
import os
from CommonAssit import TimeControl
path = r"D:\Duc\Document\Project\TSB\FPCB_Inspection\picture\Ảnh đợt 4 20211222\GLassed_HighLight\o_scratch\o1_hl.png"
time = TimeControl.time()
# image = io.imread(path)
image = cv.imdecode(np.fromfile(path, dtype=np.uint8), cv.IMREAD_COLOR)
print(TimeControl.time() - time)
cv.imshow("image", image)

cv.waitKey(0)
cv.destroyAllWindows()


'''

#         tesst serialComunication >> error
import cv2

'''
import serial
from CommonAssit import TimeControl

def readAsciiData(port):
    output = ""
    try:
        res = port.read_all()
        output += res.decode('utf-8')
    except:
        pass
    return output

def sendAsciiData(port, data):
    # if not self.isOpened:
    #     self.mainWindow.runningTab.insertLog("Serial Send Data: The port is not open!")
    #     return self.isOpened
    dataSend = str(data)
    try:
        if port.isOpen():
            port.write(dataSend.encode("utf-8"))
            # self.mainWindow.runningTab.insertLog("Serial Data Send: {}".format(data))
        else:
            # self.mainWindow.runningTab.insertLog("Cannot connect to the serial port")
            return False
    except Exception as error:
        print("ERROR Serial Send Data - ERROR; {}".format(error))
        return  False
    return True

def write_timeout_func():
    print("Timeout")



def main():
    time = TimeControl.time()

    port = serial.Serial(
        port="COM3",
        baudrate=3840,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        # write_timeout=100
        # rtscts = True
        # xonxoff=True,
        # dsrdtr=True,
    )
    # print(port.xonxoff)
    # time
    TimeControl.sleep(2000)
    sendAsciiData(port, '@00F17200E0\r\n')
    port.write_timeout = 100
    TimeControl.sleep(100)
    sendAsciiData(port, '@00O004F\r\n')

    while TimeControl.time() - time < 20000:
        data = readAsciiData(port)
        if data != "":
            print(data)
            # sendAsciiData(port, data)
if __name__ == '__main__':
    main()

'''
'''
import serial
from CommonAssit import TimeControl

def readAsciiData(port):
    output = ""
    try:
        res = port.read_all()
        output += res.decode('utf-8')
    except:
        pass
    return output

def sendAsciiData(port, data):
    # if not self.isOpened:
    #     self.mainWindow.runningTab.insertLog("Serial Send Data: The port is not open!")
    #     return self.isOpened
    dataSend = str(data)
    try:
        if port.isOpen():
            port.write(dataSend.encode("utf-8"))
            # self.mainWindow.runningTab.insertLog("Serial Data Send: {}".format(data))
        else:
            # self.mainWindow.runningTab.insertLog("Cannot connect to the serial port")
            return False
    except Exception as error:
        print("ERROR Serial Send Data - ERROR; {}".format(error))
        return  False
    return True

def write_timeout_func():
    print("Timeout")



def main():
    time = TimeControl.time()

    port = serial.Serial(
        port="COM2",
        baudrate=3840,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        # write_timeout=100
        # rtscts = True
        # xonxoff=True,
        # dsrdtr=True,
    )
    # print(port.xonxoff)
    # time
    TimeControl.sleep(2000)
    sendAsciiData(port, '@00F17200E0\r\n')
    port.write_timeout = 100
    TimeControl.sleep(100)
    sendAsciiData(port, '@00O004F\r\n')

    while TimeControl.time() - time < 20000:
        data = readAsciiData(port)
        if data != "":
            print(data)
            # sendAsciiData(port, data)
if __name__ == '__main__':
    main()
'''

# from ctypes import *
# from CommonAssit import TimeControl
# import keyboard
# from pynput.mouse import Controller
# from time import sleep
# import threading
#
# def blockinput():
#     global block_input_flag
#     block_input_flag = 1
#     t1 = threading.Thread(target=blockinput_start)
#     t1.start()
#     print("[SUCCESS] Input blocked!")
#
#
# def unblockinput():
#     blockinput_stop()
#     print("[SUCCESS] Input unblocked!")
#
# def blockinput_start():
#     mouse = Controller()
#     global block_input_flag
#     for i in range(150):
#         keyboard.block_key(i)
#     while block_input_flag == 1:
#         mouse.position = (0, 0)
#
# def blockinput_stop():
#     global block_input_flag
#     for i in range(150):
#         keyboard.unblock_key(i)
#     block_input_flag = 0
#
# blockinput()
# print("now blocking")
# TimeControl.sleep(5000)
# blockinput_stop()

import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def estimate_coef(x, y):
    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return (b_0, b_1)


def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color="m",
                marker="o", s=30)

    # # predicted response vector
    y_pred = b[0] + b[1] * x
    #
    # # plotting the regression line
    plt.plot(x, y_pred, color="g")

    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')

    # function to show plot
    plt.show()


def main():
    # observations / data
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    y = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12])

    # estimating coefficients
    b = estimate_coef(x, y)
    print("Estimated coefficients:\nb_0 = {}  \
          \nb_1 = {}".format(b[0], b[1]))

    # plotting regression line
    plot_regression_line(x, y, b)

def show_image(name, image, wait_key=0):
    cv2.imshow(name, cv2.resize(image, (800, 600)))
    cv2.waitKey(wait_key)

def image_process():
    origin_image_path = r"D:\Working\Document\Project\MES\NamViet\Gap_truc\z3539917473335_87bca221b1217b41950d9e1f53e1791e.jpg"
    image_path = r"D:\Working\Document\Project\MES\NamViet\Gap_truc\contour_1.jpg"
    image = cv2.imread(image_path)
    origin_image = cv2.imread(origin_image_path)
    print(image.shape)
    if len(image.shape) > 2:
        try:
            sourceImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except:
            sourceImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        sourceImage = image.copy()
    ret, thresh_image= cv2.threshold(sourceImage, 100, 255, type=cv2.THRESH_BINARY)

    cv2.imshow("thresh_image", cv2.resize(thresh_image, (800, 600)))
    cv2.waitKey(0)

    # finding contour
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    # color_thresh_image = cv2.cvtColor(thresh_image, c)

    for contour in contours:
    # contour_0 = contours[0]
    #     x_min = contour[:,:, 0].min()
    #     x_max = contour[:,:, 0].max()
        # points = np.empty((0, 1, 2), dtype=contour.dtype)
        # for x_value in range(x_min, x_max):
        #     x_points = contour[np.where(contour[:, :, 0] == x_value)[0]]
        #     if len(x_points) == 2:
        #         point = np.array(np.mean(x_points, axis=0, dtype=contour.dtype))
        #         points = np.concatenate([points, [point]])

        # x = points[:, : , 0]
        # y = points[:, :, 1]
        x = contour[:, : , 0]
        y = contour[:, :, 1]
        b = sk_learn_lr(x, y)

        x_min = x.min()
        x_max = x.max()
        y_min = int(b[0] + b[1] * x_min)
        y_max = int(b[0] + b[1] * x_max)
        cv2.circle(origin_image, (x_min, y_min), 30, (0, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(origin_image, (x_max, y_max), 30, (0, 255, 255), -1, cv2.LINE_AA)

        cv2.line(origin_image, (x_min, y_min), (x_max, y_max), (0, 255, 255), 6, cv2.LINE_AA)
        cv2.drawContours(image, contours, -1, (0, 255, 0), 3, cv2.LINE_AA)

        # cv2.drawContours(origin_image, points, -1, (0, 255, 0), 3, cv2.LINE_AA)

    show_image("contours", origin_image)
    cv2.destroyAllWindows()
    cv2.imwrite(r"./result.png", origin_image)

def sk_learn_lr(x, y):
    regr = LinearRegression()
    # x_reshape = x.copy().reshape(-1, 1)
    # y_reshape = y.copy().reshape(-1, 1)
    regr.fit(x,y)
    return regr.intercept_, regr.coef_[0]
    # plot_regression_line(x, y, (regr.intercept_, regr.coef_[0]))

    # print(regr.score(X_test, y_test))

def test_image():
    image = np.zeros(shape=(50, 50, 3), dtype=np.uint8)

    # observations / data
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    y = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12])

    # estimating coefficients
    b = estimate_coef(x, y)
    print("Estimated coefficients:\nb_0 = {}  \
          \nb_1 = {}".format(b[0], b[1]))
    x_min = x[0]
    x_max = x[-1]
    y_min = int(b[0] + b[1] * x_min)
    y_max = int(b[0] + b[1] * x_max)
    for x_, y_ in zip(x, y):
        cv2.circle(image, (x_, y_), 3, (0, 255, 0), -1, cv2.LINE_AA)

    cv2.circle(image, (x_min, y_min), 3, (0, 255, 255), -1, cv2.LINE_AA)
    cv2.circle(image, (x_max, y_max), 3, (0, 255, 255), -1, cv2.LINE_AA)

    cv2.line(image, (x_min, y_min), (x_max, y_max), (0, 255, 255), 2, cv2.LINE_AA)

    show_image("image", image)


if __name__ == "__main__":
    image_process()
    # test_image()
    # main()