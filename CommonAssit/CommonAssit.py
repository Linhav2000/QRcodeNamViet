import cv2 as cv
import numpy as np
from tkinter import *
from PIL import Image
from PIL import ImageTk
import glob
from multiprocessing import Process
from CommonAssit import TimeControl
import notificationcenter


def showArrayImage(_image, canvasView):
    global imagesShow
    shape = _image.shape
    # self.widthCoef = shape[1] / self.imageView.winfo_width()
    # self.heightCoef = shape[0] / self.imageView.winfo_height()

    if len(shape) == 3:
        try:
            _image = cv.cvtColor(_image, cv.COLOR_BGR2RGB)
        except:
            pass
    else:
        try:
            _image = cv.cvtColor(_image, cv.COLOR_GRAY2RGB)
        except:
            pass
    _image = cv.resize(_image, (canvasView.winfo_width(), canvasView.winfo_height()))
    try:
        imageShow = ImageTk.PhotoImage(Image.fromarray(_image))
    except:
        imageShow = ImageTk.PhotoImage(Image.fromarray((_image * 255).astype(np.uint8)))

    canvasView.create_image(0, 0, anchor=NW, image=imageShow)
    canvasView.image = imageShow

def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys


def getIndexByValue(dictOfElements, valueToFind):
    try:
        listOfKeys = list()
        listOfItems = dictOfElements.items()
        global i
        i = 0
        for item in listOfItems:
            if item[1] == valueToFind:
                listOfKeys.append(i)
            i += 1
        return listOfKeys
    except:
        pass

def ascii2Hex(asciiData):
    ret = ""
    for ch in asciiData:
        ret += hex(ord(ch))

    return ret

def getChecksum(str):
    ret = hex(sum(str.encode('ascii')) % 256)[2:]
    if len(ret) < 2:
        ret = '0' + ret
    return ret

def decimal2Hex(decimal):
    ret = hex(decimal)[2:]
    if len(ret) < 2:
        ret = '0' + ret
    return ret

def change2Format3Number(number):
    valueSend = ""
    try:
        numOfPosLengthSend = 3
        realNumOfPosLength = len(str(int(number)))
        for i in range(numOfPosLengthSend - realNumOfPosLength):
            valueSend += '0'
        valueSend = "{}{}".format(valueSend, number)
    except:
        pass
    return valueSend

import sys, os

def resource_path(relative_path):
    # if hasattr(sys, '_MEIPASS'):
        # return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
import os
def getAllImagePath(root_dir):
    time = TimeControl.time()
    _, _, image_paths = next(os.walk(root_dir), (None, None, []))
    full_paths = [os.path.join(root_dir, image_path).replace("\\", "/") for image_path in image_paths]
    # full_paths = []
    # full_paths += glob.glob(f'{root_dir}/*.jpg')
    # full_paths += glob.glob(f'{root_dir}/*.png')
    # full_paths += glob.glob(f'{root_dir}/*.bmp')
    # full_paths += glob.glob(f'{root_dir}/*.gif')
    # full_paths += glob.glob(f'{root_dir}/*.GIF')
    # full_paths += glob.glob(f'{root_dir}/*.tiff')
    # full_paths += glob.glob(f'{root_dir}/*.ico')
    # full_paths = [image_path.replace("\\", "/") for image_path in full_paths]
    print(f"Read path time = {TimeControl.time() - time}")
    # image_paths.sort()
    return full_paths

def show_loading_view():
    loading_view_thread = Process(target=show_loading_view_thread, args=())
    loading_view_thread.start()
    # loading_view_thread.join()

def show_loading_view_thread():
    import tkinter as tk
    width = 389
    height = 389
    frame = tk.Toplevel()
    frame.geometry("{}x{}".format(width, height))
    frame.resizable(0, 0)

    from View.Common.LoadingView import LoadingView
    loading_view = LoadingView()

    def loading_done(sender, notification_name, info):
        loading_view.done()
    notification_center = notificationcenter.NotificationCenter()
    notification_center.add_observer(with_block=loading_done, for_name="LoadingDone")

def getImageTypeFromName(fileName):
    fileType = ".bmp"
    new_name = fileName
    if fileName.endswith('.jpg'):
        fileType = ".jpg"
    elif fileName.endswith('.png'):
        fileType = ".png"
    elif fileName.endswith('.bmp'):
        fileType = ".bmp"
    elif fileName.endswith('.ico'):
        fileType = ".ico"
    elif fileName.endswith('.gif'):
        fileType = ".gif"
    elif fileName.endswith('.GIF'):
        fileType = ".GIF"
    elif fileName.endswith('.jpeg'):
        fileType = ".jpeg"
    else:
        fileType = ".bmp"
        new_name = fileName + ".bmp"

    return fileType, new_name

def check_sum(string_source):
    int_value = 0
    for char in string_source:
        int_value += int(format(ord(char), "x"), 16)

    return str(hex(int_value)[-2:]).upper()