from View.Common.ScrollFrame import ScrollView
import CommonAssit.CommonAssit as CommonAssit
from View.Common.VisionUI import *

class PointActivatedState(enum.Enum):
    activated = "activated"
    deactivated = "deactivated"

class ActivePointAdvanceSettingView(VisionTopLevel):
    scrollView: ScrollView
    checkAllVar: StringVar
    listPointAdvance = []
    btnOk: OkButton
    btnCancel: Button

    lastSetting = []
    result = []

    confirmYes = False

    def __init__(self, mainWindow, activeFrom, activeTo, lastSetting):
        VisionTopLevel.__init__(self)
        self.mainWindow = mainWindow
        self.activeFrom = activeFrom
        self.activeTo = activeTo
        self.lastSetting = lastSetting
        self.setupView()

    def setupView(self):
        self.settingWindow()
        self.setupScrollView()
        self.setupButtonOK()
        self.setupButtonCancel()
        self.showLastSetting()

    def setupButtonOK(self):
        self.btnOk = OkButton(self, command=self.clickBtnOK)
        self.btnOk.place(relx=0.2, rely=0.92, relwidth=0.25, relheight=0.07)

    def setupButtonCancel(self):
        self.btnCancel = CancelButton(self, command=self.clickBtnCancel)
        self.btnCancel.place(relx=0.55, rely=0.92, relwidth=0.25, relheight=0.07)
        return

    def settingWindow(self):
        width = 300
        height =500
        self.title(self.mainWindow.languageManager.localized("advanceActiveTitle"))

        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        self.geometry("{}x{}+{}+{}".format(width, height, int
        (self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - width / 2),
                                           int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - height / 2)))
        self.resizable(0, 0)
        self.grab_set()

    def setupScrollView(self):
        self.listPointAdvance = []
        self.checkAllVar = StringVar()
        self.scrollView = ScrollView(self, scrollWidth=200,scrollHeight=1000)
        self.scrollView.place(relx=0, rely=0, relwidth=1, relheight=0.9)
        selectAllFrame = VisionFrame(self.scrollView.view, width=self.winfo_width(), height=30)
        selectAllLabel = VisionLabel(selectAllFrame, text=self.mainWindow.languageManager.localized("selectAll"), font=('Helvetica', 10, 'bold'))
        selectAllLabel.place(relx=0.2, rely =0)

        self.selectAllCheckBox = Checkbutton(selectAllFrame, command=self.clickSelectAll, variable=self.checkAllVar,
                                          onvalue="selected", offvalue="unselected")
        self.selectAllCheckBox.deselect()
        self.selectAllCheckBox.place(relx=0.65, y=5, width=28, height=20)
        selectAllFrame.grid(row=0, column=1)

        for row in range(self.activeTo - self.activeFrom + 1):
            pointAdvance = PointAdvance(self.scrollView.view, self.mainWindow, orderIndex=(row + self.activeFrom) , width=self.winfo_width())
            pointAdvance.grid(row=row + 1, column=1)
            self.listPointAdvance.append(pointAdvance)

    def clickSelectAll(self):
        if self.checkAllVar.get() == "selected":
            for pointAdvance in self.listPointAdvance:
                pointAdvance.select()
        else:
            for pointAdvance in self.listPointAdvance:
                pointAdvance.deselect()

    def showLastSetting(self):
        if len(self.lastSetting) <= 0 or int(self.lastSetting[0][0]) != self.activeFrom or int(self.lastSetting[len(self.lastSetting ) - 1][0]) != self.activeTo:
            self.selectAllCheckBox.select()
            self.clickSelectAll()
        else:
            for index in range(len(self.listPointAdvance)):
                self.listPointAdvance[index].chosenVar.set(self.lastSetting[index][1])

    def clickBtnOK(self):
        self.result = []
        for pointAdvance in self.listPointAdvance:
            self.result.append([pointAdvance.orderIndex, pointAdvance.chosenVar.get()])
        self.confirmYes = True
        self.destroy()

    def clickBtnCancel(self):
        self.confirmYes = False
        self.destroy()

class PointAdvance(VisionFrame):
    chosenCheckBox: Checkbutton
    chosenVar: StringVar
    def __init__(self, master, mainWindow, orderIndex, width = 200):
        VisionFrame.__init__(self, master=master, width = width, height=30)
        self.orderIndex = orderIndex
        self.mainWindow = mainWindow
        self.setupView()

    def setupView(self):
        border = VisionLabelFrame(self)
        border.place(relx=0.2, rely=0, relwidth=0.6, relheight=1)

        label = VisionLabel(border, text="{} {}".format(self.mainWindow.languageManager.localized("point"), self.orderIndex))
        label.place(relx=0, rely=0)

        self.chosenVar = StringVar()
        self.chosenCheckBox = Checkbutton(border, command=self.checkedChosenBox, variable=self.chosenVar,
                                          onvalue=PointActivatedState.activated.value, offvalue=PointActivatedState.deactivated.value)
        self.chosenCheckBox.deselect()
        self.chosenCheckBox.place(relx=0.75, y=5, width=28, height=20)

    def checkedChosenBox(self):
        return

    def select(self):
        self.chosenCheckBox.select()

    def deselect(self):
        self.chosenCheckBox.deselect()