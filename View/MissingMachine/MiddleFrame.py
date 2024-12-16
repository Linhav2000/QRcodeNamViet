from CommonAssit import VisionFont
from View.Common.Clock import Clock
from View.Common.VisionUI import *
from View.Common.LogoView import LogoView
from View.Common.ImageView import ImageView
from Modules.CheckMissing.NgImageView import NgImageView
import copy

class MiddleFrame(VisionFrame):
    btnStart: ImageButton
    btnExit: TeachingButton
    clock: Clock
    start_btnImage: Image
    stop_btnImage: Image
    logoView: LogoView
    ngImageViewList = []
    ngImageList = []
    currentStates = [True, True]
    currentImages = [None, None]

    LEFT_IDX = 0
    RIGHT_IDX = 1

    def __init__(self, master, mainWindow):
        from View.MissingMachine.MissingMachineResultWindow import MissingMachineResultWindow
        VisionFrame.__init__(self, master=master)
        self.missingResultWindow: MissingMachineResultWindow = master
        self.mainWindow = mainWindow
        self.setupView()

    def setupView(self):

        # # Clock
        # self.clock = Clock(self)
        # self.clock.place(relx=0, rely=0.01, relwidth=1)
        # self.clock.config(font=Font.regularFont(16), fg=Color.resultBg(), anchor="center")

        self.logView = Text(self, fg=Color.winRed(), font=VisionFont.boldFont(10))
        self.logView.place(relx=0, rely=0, relwidth=1, relheight=0.04)
        self.logView.insert(END, 'This is first log')

        self.modelFrame = VisionLabelFrame(self, text="Model")
        self.modelFrame.place(relx=0.05, rely=0.04, relwidth=0.9, relheight=0.06)

        self.modelName = VisionLabel(self.modelFrame, text="Model name", font=VisionFont.boldFont(14))
        self.modelName.place(relx=0.0, rely=0, relwidth=1, relheight=1)

        self.btnStart = StartButton(self, command=self.clickBtnStart)
        # self.btnStart.place(relx=0.25, rely=0.21, relwidth=0.5, relheight=0.1)
        self.btnStart.place(relx=0.02, rely=0.11, relwidth=0.45, relheight=0.08)

        self.btnExit = TeachingButton(self, command=self.clickBtnExit)
        self.btnExit.place(relx=0.52, rely=0.11, relwidth=0.45, relheight=0.08)

        self.logoView = LogoView(self, imagePath="./resource/logo.png")
        self.logoView.place(relx=0.05, rely=0.89, relwidth=0.9, relheight=0.1)

        self.leftImage1 = ImageView(self, self.mainWindow)
        self.leftImage2 = ImageView(self, self.mainWindow)
        self.leftImage3 = ImageView(self, self.mainWindow)

        self.rightImage1 = ImageView(self, self.mainWindow)
        self.rightImage2 = ImageView(self, self.mainWindow)
        self.rightImage3 = ImageView(self, self.mainWindow)


        self.leftImage1.place(relx=0, rely=0.2, relwidth=0.48, relheight=0.13)
        self.rightImage1.place(relx=0.52, rely=0.2, relwidth=0.48, relheight=0.13)

        self.leftImage2.place(relx=0, rely=0.33, relwidth=0.48, relheight=0.13)
        self.rightImage2.place(relx=0.52, rely=0.33, relwidth=0.48, relheight=0.13)

        self.leftImage3.place(relx=0, rely=0.46, relwidth=0.48, relheight=0.13)
        self.rightImage3.place(relx=0.52, rely=0.46, relwidth=0.48, relheight=0.13)

        self.ngImageViewList = [
            NgImageView(self.mainWindow, self.leftImage1, self.rightImage1),
            NgImageView(self.mainWindow, self.leftImage2, self.rightImage2),
            NgImageView(self.mainWindow, self.leftImage3, self.rightImage3)
        ]

    def resetCurrentState(self):
        self.currentStates = [True, True]
        self.currentImages = [None, None]

    def setLeftImage(self, state, image):
        self.currentStates[self.LEFT_IDX] = state
        self.currentImages[self.LEFT_IDX] = image.copy()
        self.showNGImage()
        self.resetCurrentState()

    def setRightImage(self, state, image):
        self.currentStates[self.RIGHT_IDX] = state
        self.currentImages[self.RIGHT_IDX] = image.copy()
        self.showNGImage()

    def showNGImage(self):
        if self.currentStates[self.RIGHT_IDX] and self.currentStates[self.LEFT_IDX]:
            return
        else:
            # self.ngImageViewList[0].setImage(leftImage=self.currentImages[self.LEFT_IMAGE_IDX], rightImage=self.currentImages[self.RIGHT_IMAGE_IDX])
            self.addNewNGImage()

    def addNewNGImage(self):
        try:
            if len(self.ngImageList) >= 3:
                if self.currentImages[self.LEFT_IDX] is None:
                    self.ngImageList.__delitem__(len(self.ngImageList) - 1)
                    self.ngImageList.insert(0, self.currentImages)
                else:
                    if not self.currentStates[self.LEFT_IDX] and self.currentStates[self.RIGHT_IDX]:
                        self.ngImageList.insert(0, self.currentImages)
                    else:
                        self.ngImageList[0] = copy.deepcopy(self.currentImages)
            else:
                if self.currentImages[self.LEFT_IDX] is None:
                    self.ngImageList.insert(0, self.currentImages)
                else:
                    if not self.currentStates[self.LEFT_IDX] and self.currentStates[self.RIGHT_IDX]:
                        self.ngImageList.insert(0, self.currentImages)
                    else:
                        self.ngImageList[0] = copy.deepcopy(self.currentImages)

            while len(self.ngImageList) > 3:
                self.ngImageList.__delitem__(len(self.ngImageList) - 1)

            for i in range(len(self.ngImageList)):
                self.ngImageViewList[i].setImage(leftImage=self.ngImageList[i][self.LEFT_IDX],
                                                 rightImage=self.ngImageList[i][self.RIGHT_IDX])
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Update new NG image: {}".format(error))
            print("ERROR Update new NG image: {}".format(error))
            pass

    def clickBtnExit(self):
        self.missingResultWindow.exit()

    def clickBtnStart(self):
        if self.mainWindow.runningTab.clickBtnStart():
            self.updateStartButton()
            return True
        else:
            return False

    def updateStartButton(self):
        self.btnStart.setImagePath(imagePath="./resource/start_button.png"if not self.mainWindow.workingThread.runningFlag else "./resource/stop_button.png")

    def updateModelName(self):
        try:
            name = self.mainWindow.modelSettingTab.modelManager.models[self.mainWindow.modelSettingTab.modelManager.currentModelPos].name
        except:
            name = "Model Name"
        self.modelName.config(text=name)

    def insertLog(self, log):
        self.logView.insert(END, "\n{}".format(log))
        self.logView.see(END)