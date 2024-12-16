import tkinter.messagebox as messagebox
import CommonAssit.CommonAssit as CommonAssit
from View.Common.VisionUI import *
from View.Common.CommonStepFrame import *


class ImageViewSettingWindow(VisionTopLevel):

    btnSave: Button
    btnCancel: Button
    relWidth: InputParamFrame
    relHeight: InputParamFrame

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        VisionTopLevel.__init__(self)
        self.bind("<Return>", self.push_enter)
        self.mainWindow: MainWindow = mainWindow
        self.windowSetting()
        self.setupView()

    def push_enter(self, event):
        self.save()

    def windowSetting(self):
        self.title("Image View Setting")
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        self.geometry("436x222+{}+{}".format(
            int(self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - 436 / 2),
            int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - 222 / 2)))
        self.resizable(0, 0)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.close)

    def setupView(self):
        self.relWidth = InputParamFrame(self, "Related Width Value:", yPos=15, height=35)
        self.relHeight = InputParamFrame(self, "Related Height Value:", yPos=15 + 35, height=35)

        self.relWidth.setValue(self.mainWindow.commonSettingManager.settingParm.imageViewDimension[0])
        self.relHeight.setValue(self.mainWindow.commonSettingManager.settingParm.imageViewDimension[1])

        self.btnSave = SaveButton(self, command=self.save)
        self.btnSave.place(relx=0.2, y=120, relwidth=0.25, height=40)

        self.btnCancel = CancelButton(self, command=self.close)
        self.btnCancel.place(relx=0.55, y=120, relwidth=0.25, height=40)

    def save(self):
        relWidth = self.relWidth.getFloatValue()
        relHeight = self.relHeight.getFloatValue()
        if relWidth > 1 or relHeight > 1 or relWidth <=0 or relHeight <= 0:
            messagebox.showerror("Invalid Value", "Related Width and Height Value are only valid in range of (0.0 : 1.0)")
            return
        self.mainWindow.commonSettingManager.settingParm.imageViewDimension = (relWidth, relHeight)
        self.mainWindow.commonSettingManager.save()
        self.mainWindow.changeImageViewSetting()
        self.destroy()

    def close(self):
        if self.dataIsChanged():
            ask = messagebox.askyesno("Save information", "Do you want to save Image View Setting?")
            if ask:
                self.save()

        self.destroy()

    def dataIsChanged(self):
        return self.mainWindow.commonSettingManager.settingParm.imageViewDimension != (self.relWidth.getFloatValue(), self.relHeight.getFloatValue())
