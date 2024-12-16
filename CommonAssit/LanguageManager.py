import os
import tkinter.messagebox as messagebox
from CommonAssit.FileManager import *
from CommonAssit import PathFileControl

class LanguageManager:
    viewPath = "./View"
    currentLanguage = 0
    lastLanguage = 0
    englishDict = {}
    vietnameseDict = {}
    lang_dict = {}
    lang_list = []
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.getDictFromCSV()
        self.getCurrentLaguage()

    def getDictionary(self):
        self.englishDict = self.readDict("./resource/Languages/English.txt")
        self.vietnameseDict = self.readDict("./resource/Languages/Vietnamese.txt")

    def getDictFromCSV(self):
        self.lang_dict = {}
        csvFile = CsvFile("./resource/Languages/Multi_Language.csv")
        data_list = csvFile.readFile()
        self.lang_list = []
        for i in range(1, len(data_list[1])):
            self.lang_dict[data_list[1][i]] = {}
            self.lang_list.append(data_list[1][i])

        for i in range(2, len(data_list)):
            for j, lang in enumerate(self.lang_list):
                self.lang_dict[lang][data_list[i][0]] = data_list[i][j + 1]

    def readDict(self, path):
        dict = {}
        textFile = TextFile(path)
        textFile.readFile()
        try:
            for result in textFile.dataList:
                try:
                    key, value = result.split("=")
                    if value.endswith("\n"):
                        value = value[:-1]
                    if value.__contains__("\\n"):
                        value = value.replace("\\n", "\n")
                    dict[key] = value
                except:
                    pass
        except:
            pass
        return dict

    def changeLanguage(self, language):
        self.lastLanguage = self.currentLanguage
        self.currentLanguage = self.lang_list.index(language)
        self.saveCurrentLanguage()
        self.mainWindow.notificationCenter.post_notification(sender=None, with_name="ChangeLanguage")


    def localized(self, key):
        return self.lang_dict[self.lang_list[self.currentLanguage]][key]

    def localizedLastLanguage(self, key):
        return self.lang_dict[self.lang_list[self.lastLanguage]][key]

    def getCurrentLaguage(self):
        path = "./config/CurrentLanguage.txt"
        PathFileControl.generatePath("./config")

        file = TextFile(path)
        file.readFile()
        try:
            self.currentLanguage = int(file.dataList[0])
            self.lastLanguage = int(file.dataList[0])
        except:
            self.currentLanguage = 0
            self.lastLanguage = 0

    def saveCurrentLanguage(self):
        path = "./config/CurrentLanguage.txt"
        PathFileControl.generatePath("./config")

        file = TextFile(path)
        file.dataList = [self.currentLanguage]
        file.saveFile()
