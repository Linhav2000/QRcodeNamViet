import tkinter.messagebox as messagebox
import CommonAssit.CommonAssit as CommonAssit
from View.Common.VisionUI import *

class NewModelView(VisionTopLevel):

    btnSave: Button
    btnCancel: Button
    nameEntry: VisionEntry
    nameLabel : VisionLabel
    def __init__(self, mainWindow, modelManager):
        from MainWindow import MainWindow
        from Modules.ModelSetting.ModelManager import ModelManager
        VisionTopLevel.__init__(self)
        self.mainWindow: MainWindow = mainWindow
        self.modelManager: ModelManager = modelManager
        self.windowSetting()
        self.createView()
        self.notifyRegister()

    def windowSetting(self):
        self.title("New Model")
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        self.geometry("436x222+{}+{}".format(
            int(self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - 436 / 2),
            int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - 222 / 2)))
        self.bind("<Return>", self.push_enter)
        self.resizable(0, 0)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.close)

    def push_enter(self, event):
        self.save()
    def notifyRegister(self):
        self.mainWindow.notificationCenter.add_observer(with_block=self.changeLanguage, for_name="ChangeLanguage")
    def changeLanguage(self, sender, notification_name, info):
        self.nameLabel.config(text=self.mainWindow.languageManager.localized("model name"))
    def createView(self):
        self.nameLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("model name"))
        self.nameLabel.place(x=10, y=30)
        self.nameEntry = VisionEntry(self)
        self.nameEntry.place(relx=0.22, y=30, relwidth=0.7, height=25)
        self.nameEntry.focus_set()

        self.btnSave = SaveButton(self, command=self.save)
        self.btnSave.place(relx=0.2, y=120, relwidth=0.25, height=40)

        self.btnCancel = CancelButton(self, command=self.close)
        self.btnCancel.place(relx=0.55, y=120, relwidth=0.25, height=40)


    def close(self):
        if self.dataIsChanged():
            ask = messagebox.askyesno("Save information", "Do you want to save Model")
            if ask:
                self.save()

        self.destroy()

    def dataIsChanged(self):
        if self.nameEntry.get() != "":
            return True
        else:
            return False

    def save(self):
        from Modules.ModelSetting.ModelParameter import ModelParameter
        modelName = self.nameEntry.get()
        if modelName == "":
            messagebox.showerror("Input Name", "Please input the model name!")
            return

        if self.modelManager.modelNameExisted(modelName):
            messagebox.showerror("Model Name", "Model name is existed, Please input another name!")
            return

        try:
            model = ModelParameter()
            model.name = modelName
            self.modelManager.addNew(model)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save model: {}".format(error))
            messagebox.showerror("Save model", "".format(error))
        self.destroy()
        self.mainWindow.notificationCenter.post_notification(sender=None, with_name="UpdateListModel")
        return