from CommonAssit import TimeControl
import random
import sys
from ctypes import *
from CommonAssit import PathFileControl
from CommonAssit.FileManager import TextFile
from getpass import getpass

from CommonAssit import InternetSupport


def runActive():
    userName = "phamduc0810@gmail.com"
    password = "@Cunduc0810"
    listModules = [
        "Basler Camera",
        "Point Grey camera",
        "Csr Camera",
        "Hik camera",
        "Webcam camera",
        "OpenCv for window",
        "Numpy for window",
        "Pypylon for window",
        "Cython for window",
        "Python",
        "Pycapture2",
        "PyQt for window",
        "Json for window",
        "File access",
        "Notebook",
        "Pyflycapture",
        "Pyserial",
        "tensorFlow environment",
        "Wheel package",
        "Virtual environment",
        "zip",
        "gxip",
        "xcyp",
        "pyspin",
        "pefile",
        "pipevn",
        "matplotlib",
        "hikvison api",
        "File lock",
        "Config Parser"
        "Image process",
        "Log data",
        "Camera control",
        "Light controller",
        "Ethernet controller"
        "Socket manager"
    ]

    print("Welcome to Magic Vision")
    print("To use our product please first active all modules")

    inputUserName = ""
    inputPW = ""
    try:
        inputUserName = input("Login to active all current modules: \nUser name:    ")
        inputPW = getpass()
    except:
        pass

    if inputUserName != userName or inputPW != password:
        print("The Active information is invalid!\nPlease try again, or check the account!")
        print("Active the application failed!")
        if PathFileControl.pathExisted("C:\\Document\\VS\\state.txt"):
            PathFileControl.deleteFile(path="C:\\Document\\VS\\state.txt")
        sys.exit()

    for module in listModules:
        print("Activating module {}.....".format(module))
        delay = random.randint(3, 8)
        TimeControl.sleep(delay * 1000)
        print("Activate module {} : Done 100%".format(module))
        TimeControl.sleep(500)

    documentPath = "C:\\Document"
    vsPath = "C:\\Document\\VS"
    activeFilePath = "C:\\Document\\VS\\state.txt"

    PathFileControl.generatePath(documentPath)
    PathFileControl.generatePath(vsPath)

    activeFile = TextFile(activeFilePath)
    time = 8101112
    activeFile.dataList = [f"{time}"]
    activeFile.saveFile()

    windll.kernel32.SetFileAttributesW(vsPath, 2)
    print("Active application successfully!")


if __name__ == '__main__':
    if InternetSupport.have_internet():
        runActive()
    else:
        print("Cannot connect to the internet, please connect to the internet first!")
        print("If there is no internet connection, please change to offline active")
        inputChosen = input("Do you want to change to offline active Y/N ? :  ")

        if inputChosen == "Y" or inputChosen == "y":
            runActive()
