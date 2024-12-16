import tkinter.messagebox as messagebox
import CommonAssit.CommonAssit as CommonAssit
from View.Common.VisionUI import *


class NewAlgorithmView(VisionTopLevel):

    btnSave: Button
    btnCancel: Button
    nameEntry: VisionEntry
    save_name = None
    def __init__(self, mainWindow, default_name=""):
        from MainWindow import MainWindow
        VisionTopLevel.__init__(self)
        self.bind("<Return>", self.push_enter)
        self.mainWindow: MainWindow = mainWindow
        self.default_name = default_name
        self.windowSetting()
        self.createView()

    def push_enter(self, event):
        self.save()

    def windowSetting(self):
        self.title("New Algorithm")
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        self.geometry("536x222+{}+{}".format(
            int(self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - 436 / 2),
            int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - 222 / 2)))
        self.resizable(0, 0)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.close)

    def createView(self):

        nameLabel = VisionLabel(self, text="Algorithm name : ")
        nameLabel.place(x=10, y=30)
        self.nameEntry = VisionEntry(self)
        self.nameEntry.place(relx=0.33, y=30, relwidth=0.6, height=25)
        self.nameEntry.insert(0, self.default_name)
        self.nameEntry.focus_set()

        self.btnSave = SaveButton(self, command=self.save)
        self.btnSave.place(relx=0.2, y=120, relwidth=0.25, height=40)

        self.btnCancel = CancelButton(self, command=self.close)
        self.btnCancel.place(relx=0.55, y=120, relwidth=0.25, height=40)


    def close(self):
        if self.dataIsChanged():
            ask = messagebox.askyesno("Save information", "Do you want to save Algorithm")
            if ask:
                self.save()

        self.destroy()

    def dataIsChanged(self):
        if self.nameEntry.get() != "":
            return True
        else:
            return False

    def save(self):
        algorithmName = self.nameEntry.get()
        if algorithmName == "":
            messagebox.showerror("Input Name", "Please input the algorithm name!")
            return

        if self.mainWindow.algorithmManager.algorithmNameExisted(algorithmName):
            messagebox.showerror("Algorithm name", "Algorithm name is existed, Please input another name!")
            return

        try:
            self.mainWindow.algorithmManager.addNewAlgorithm(algorithmName)
            self.save_name = algorithmName
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Algorithm : {}".format(error))
            messagebox.showerror("Save Algorithm", "".format(error))
        self.mainWindow.tabBar.select(1)
        self.destroy()