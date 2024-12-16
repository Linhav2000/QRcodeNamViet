from CommonAssit.FileManager import JsonFile
from Modules.AxisSystem.AS_Parameter import AS_Parameter
import jsonpickle
from tkinter import messagebox
from CommonAssit import PathFileControl
from CommonAssit.FileManager import TextFile


class AS_Manager:
    filePath = "./config/AxisSystem.json"
    as_list = []
    # currentIndex = -1
    currentName = ""
    nameList = []
    jsonDatas = []

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.get()

    def save(self):
        self.jsonDatas = []
        jsonCurrent = {"currentASName": self.currentName}
        self.jsonDatas.append(jsonCurrent)
        for as_param in self.as_list:
            jsonParameter = {}
            try:
                jsonParameter = jsonpickle.encode(as_param)
            except Exception as error:
                messagebox.showerror("Save Axis System", "Cannot save this Axis System\n detail error: {}".format(error))

            self.jsonDatas.append(jsonParameter)
        paramFile = JsonFile(self.filePath)
        paramFile.data = self.jsonDatas
        paramFile.saveFile()

    def get(self):
        self.as_list.clear()
        self.jsonDatas = []
        paramFile = JsonFile(self.filePath)
        paramFile.readFile()
        self.jsonDatas = paramFile.data

        count = 0
        for data in self.jsonDatas:
            if count == 0:
                try:
                    if "currentASName" in data.keys():
                        try:
                            self.currentName = data['currentASName']
                        except Exception as error:
                            self.mainWindow.runningTab.insertLog("ERROR get current Axis System")
                            messagebox.showerror("Get current Model", "{}".format(error))
                        count += 1
                        continue
                except:
                    count += 1
            else:
                count += 1

            as_parameter = AS_Parameter()

            try:
                as_parameter = jsonpickle.decode(data)
            except Exception as error:
                messagebox.showerror("Get Axis System setting", "{}".format(error))

            # as_parameter.makeStandardType()
            self.as_list.append(as_parameter)

    def as_name_existed(self, algorithmName):
        for as_parameter in self.as_list:
            if as_parameter.name == algorithmName:
                return True
        return False

    def addNewAxisSystem(self, as_name):
        as_parameter = None
        try:
            as_parameter = AS_Parameter()
            as_parameter.name = as_name
            self.as_list.append(as_parameter)
            self.save()
            self.currentName = as_parameter.name
            self.mainWindow.as_setting_tab.updateParameterForNewList()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Add New Axis System: {}".format(error))
            messagebox.showerror("Add New Axis System", "{}".format(error))
        return as_parameter

    def addAxisSystem(self, new_as):
        try:
            self.as_list.append(new_as)
            self.save()
            self.currentName = new_as.name
            self.mainWindow.as_setting_tab.updateParameterForNewList()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Add New Axis System: {}".format(error))
            messagebox.showerror("Add New Axis System", "{}".format(error))

    def deleteCurrentAS(self):
        for as_param in self.as_list:
            if as_param.name == self.currentName:
                self.as_list.remove(as_param)
                break
        self.save()

    def changeCurrentAS(self, as_name):
        self.currentName = as_name
        self.save()

    def getCurrentAS(self):
        if self.getAS_WithName(self.currentName) is not None:
            return self.getAS_WithName(self.currentName)

        if len(self.as_list) > 0:
            return self.as_list[0]

        return None

    def getAS_WithName(self, name):
        for as_parameter in self.as_list:
            if as_parameter.name == name:
                return as_parameter
        return None

    def getNameList(self):
        self.nameList = []
        for as_param in self.as_list:
            self.nameList.append(as_param.name)
        return self.nameList

    def getCurrentPos(self):
        try:
            return self.nameList.index(self.currentName)
        except:
            if len(self.nameList) > 1:
                return 0
            else:
                return None