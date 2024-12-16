import csv
import json
from os import path
import tkinter.messagebox

class CsvFile:
    dataList = []

    def __init__(self, filePath):
        self.filePath = filePath
        self.dataList.clear()
        if not path.exists(self.filePath):
            self.createFile()

    def readFile(self):
        try:
            self.dataList.clear()
            with open(self.filePath, encoding="utf-8") as csvFile:
                csvReader = csv.reader(csvFile, delimiter=',')
                for row in csvReader:
                    self.dataList.append(row)

                csvFile.close()
            return self.dataList
        except Exception as error:
            print("Cannot read file {}. Detail: {}".format(self.filePath, error))

    def saveFile(self):
        with open(self.filePath, mode='w', newline='', encoding="utf-8") as csvFile:

            saveFile = csv.writer(csvFile, delimiter=',')
            for row in self.dataList:
                saveFile.writerow(row)
            csvFile.close()

    def appendData(self, data, isList=False):
        self.dataList.clear()
        if isList:
            self.dataList = data
        else:
            self.dataList.append(data)
        with open(self.filePath, mode='a+', newline='', encoding="utf-8") as csvFile:

            saveFile = csv.writer(csvFile, delimiter=',')
            for row in self.dataList:
                saveFile.writerow(row)
            csvFile.close()

    def createFile(self):
        try:
            file = open(self.filePath, "w+", encoding="utf-8")
            file.write("")
            file.close()
        except:
            pass

class TextFile:
    dataList = []

    def __init__(self, filePath):
        self.filePath = filePath
        if not path.exists(self.filePath):
            self.createFile()

    def readFile(self):
        try:
            self.dataList.clear()
            with open(self.filePath, encoding="utf-8", mode="r") as file:
                self.dataList = file.readlines()
                file.close()
            return self.dataList
        except Exception as error:
            print("Cannot read file {}. Detail: {}".format(self.filePath, error))
            return []

    def saveFile(self):
        with open(self.filePath, mode='w', newline='\r\n', encoding="utf-8") as file:
            for data in self.dataList:
                file.writelines(str(data))
            file.close()

    def appendData(self, data):
        # self.dataList.clear()
        # self.dataList.append(data)
        with open(self.filePath, mode='a+', newline='', encoding="utf-8") as file:
            try:
                file.writelines(data + "\r\n")
                file.close()
            except Exception as error:
                print("ERROR Save File Error : {}".format(error))
                tkinter.messagebox.showerror("Save File Error", "{}".format(error))

    def createFile(self):
        try:
            file = open(self.filePath, "w+", encoding="utf-8")
            file.write("")
            file.close()
        except:
            pass

class JsonFile:
    data = ""

    def __init__(self, filePath):
        self.filePath = filePath
        if not path.exists(self.filePath):
            self.createFile()

    def readFile(self):
        try:
            # self.data.clear()
            with open(self.filePath, encoding="utf-8") as file:
                self.data = json.load(file)
                file.close()
            return self.data
        except Exception as error:
            print("Cannot read file {}. Detail: {}".format(self.filePath, error))
            return self.data

    def saveFile(self):
        with open(self.filePath, mode='w', newline='', encoding="utf-8") as file:
            json.dump(self.data, file)
            file.close()

    def writeData(self, data):
        self.data = ""
        self.data = data
        self.saveFile()

    def createFile(self):
        try:
            file = open(self.filePath, "w+", encoding="utf-8")
            json.dump(self.data, file)
            file.close()
        except:
            pass