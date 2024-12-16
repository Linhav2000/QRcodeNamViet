from CommonAssit.FileManager import JsonFile
from Modules.ModelSetting.ModelParameter import ModelParameter
import jsonpickle
from tkinter import messagebox


class ModelManager:
    currentModelPos = 0
    models = []
    jsonDatas = []

    def __init__(self):
        self.getParameter()

    def refresh(self):
        self.getParameter()

    def save(self):
        self.jsonDatas = []
        jsonCurrentModel = {"currentModelPos": self.currentModelPos}
        self.jsonDatas.append(jsonCurrentModel)
        for model in self.models:
            jsonModel = {}
            try:
                jsonModel = jsonpickle.encode(model)
            except Exception as error:
                messagebox.showerror("Save Model", "Cannot save this model\n detail error {}".format(error))

            self.jsonDatas.append(jsonModel)
        parameterPath = "./config/model.json"
        paramFile = JsonFile(parameterPath)
        paramFile.data = self.jsonDatas
        paramFile.saveFile()
        # print(paramFile.data)

    def getParameter(self):
        self.models.clear()
        self.jsonDatas = []
        parameterPath = "./config/model.json"
        paramFile = JsonFile(parameterPath)
        paramFile.readFile()
        self.jsonDatas = paramFile.data

        count = 0
        for data in self.jsonDatas:
            if count == 0:
                try:
                    if "currentModelPos" in data.keys():
                        try:
                            self.currentModelPos = int(data['currentModelPos'])
                        except Exception as error:
                            messagebox.showerror("Get current Model", "{}".format(error))
                        count += 1
                        continue
                except:
                    count += 1
            else:
                count += 1

            model = ModelParameter()

            try:
                model = jsonpickle.decode(data)
            except Exception as error:
                messagebox.showerror("Get model setting", "{}".format(error))

            model.makeStandardType()
            self.models.append(model)

    def getCurrentModel(self):
        if len(self.models) < 1:
            return None
        return self.models[self.currentModelPos]

    def getModelByName(self, modelName):
        text = ""
        try:
            for model in self.models:
                if model.name == modelName:
                    return model, text
            text = "Cannot find the model with model name {}. Please check model name!".format(modelName)
            return None, text
        except Exception as error:
            text = "Cannot find the model. check model name. Detail: {}".format(error)
            return None, text

    def addNew(self, model):
        jsonModel = {}
        try:
            jsonModel = jsonpickle.encode(model)
        except Exception as error:
            messagebox.showerror("Save Model", "Cannot save this model\n detail error {}".format(error))

        self.jsonDatas.append(jsonModel)
        parameterPath = "./config/model.json"
        paramFile = JsonFile(parameterPath)
        paramFile.data = self.jsonDatas
        paramFile.saveFile()

    def modelNameExisted(self, modelName):
        for model in self.models:
            if model.name == modelName:
                return True

        return False
