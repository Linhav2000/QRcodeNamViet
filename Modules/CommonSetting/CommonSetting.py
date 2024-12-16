from CommonAssit.FileManager import *
import jsonpickle
from Modules.MachineSetting.MachineList import MachineList

class CommonSettingParm:
    currentCamera = 0
    communicationType = "serial"
    currentMachine = MachineList.all.value
    printLogFlag = False
    showAlgorithmForCurrentModelFlag = False
    use_AI = False
    cutImageSaveDir = ""
    draw_rectangle = True
    draw_circle = False
    imageResultFrameVisible = True
    imageViewDimension = (1.0, 1.0)

class CommonSettingManager:
    filePath = "./config/common_setting.json"
    settingParm: CommonSettingParm
    def __init__(self, mainWindow):
        self.settingParm = CommonSettingParm()
        self.mainWindow = mainWindow
        self.get()

    def save(self):
        try:
            file = JsonFile(self.filePath)
            jsonData = jsonpickle.encode(self.settingParm)
            file.data = jsonData
            file.saveFile()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Common setting: {}".format(error))

    def get(self):
        try:
            file = JsonFile(self.filePath)
            jsonData = file.readFile()
            self.settingParm = jsonpickle.decode(jsonData)

            machine_name_file = TextFile("./config/machine_name.txt")
            machine_name_list = machine_name_file.readFile()
            machine_name_list = [(machineName[:-1] if machineName.endswith("\n") else machineName) for machineName in machine_name_list]
            self.settingParm.currentMachine = machine_name_list[0]
        except Exception as error:
            try:
                self.mainWindow.runningTab.insertLog("ERROR Get common setting: {}".format(error))
            except:
                pass
