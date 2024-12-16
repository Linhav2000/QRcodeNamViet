import cv2 as cv
from View.Common.VisionUI import *
from CommonAssit import TimeControl
from ImageProcess.Algorithm.MethodList import MethodList

class RightClickImageOption(VisionMenu):

    startX = 0
    startY = 0
    endX = 0
    endY = 0
    processImage = None

    circle_center = (0, 0)
    circle_radius = 1

    def __init__(self, master, mainWindow):
        from MainWindow import MainWindow
        VisionMenu.__init__(self, master=master, tearoff=0)
        self.mainWindow: MainWindow = mainWindow
        self.setupCommand()

    def setParameter(self, processImage, startX=0, endX=0, startY=0, endY=0, circle_center=(0, 0), circle_radius=1):
        if self.mainWindow.commonSettingManager.settingParm.draw_rectangle:
            self.startX = startX
            self.startY = startY
            self.endX = endX
            self.endY = endY
        else:
            self.circle_center = circle_center
            self.circle_radius = circle_radius
        self.processImage = processImage.copy()

    def setupCommand(self):
        self.add_command(label="Zoom", command=self.clickZoom)
        self.add_command(label="Add Reference Image", command=self.clickAddRefImage)
        if self.mainWindow.researchingTab.isSettingStepFlag:
            self.add_command(label="Add Template", command = self.clickAddTemplate)
            self.add_command(label="Add working area", command=self.clickAddWorkingArea)
            if self.mainWindow.researchingTab.stepSettingFrame.stepParameter.stepAlgorithmName == MethodList.ignore_areas.value:
                self.add_command(label="Add ignore area", command=self.clickAddIgnoreArea)
            if self.mainWindow.researchingTab.stepSettingFrame.stepParameter.stepAlgorithmName == MethodList.multi_select_area.value:
                self.add_command(label="Add select area", command=self.click_add_select_area)
            self.add_command(label="Add BS process working area", command=self.clickAddBS_ProcessWorkingArea)
            self.add_command(label="Add paint area", command=self.clickAddPaintArea)
            self.add_command(label="Add color range", command=self.clickAddColorRange)


    def clickAddIgnoreArea(self):
        if self.mainWindow.commonSettingManager.settingParm.draw_rectangle:
            self.mainWindow.researchingTab.stepSettingFrame.add_ignore_area((self.mainWindow.basePoint[0] + self.startX,
                                                                            self.mainWindow.basePoint[1] + self.startY,
                                                                            self.mainWindow.basePoint[0] + self.endX,
                                                                            self.mainWindow.basePoint[1] + self.endY),
                                                                            "rectangle")
        elif self.mainWindow.commonSettingManager.settingParm.draw_circle:
            self.mainWindow.researchingTab.stepSettingFrame.add_ignore_area((self.circle_center, self.circle_radius),
                                                                            "circle")
    def click_add_select_area(self):
        if self.mainWindow.commonSettingManager.settingParm.draw_rectangle:
            self.mainWindow.researchingTab.stepSettingFrame.add_select_area((self.mainWindow.basePoint[0] + self.startX,
                                                                            self.mainWindow.basePoint[1] + self.startY,
                                                                            self.mainWindow.basePoint[0] + self.endX,
                                                                            self.mainWindow.basePoint[1] + self.endY),
                                                                            "rectangle")
        elif self.mainWindow.commonSettingManager.settingParm.draw_circle:
            self.mainWindow.researchingTab.stepSettingFrame.add_select_area((self.circle_center, self.circle_radius),
                                                                            "circle")

    def clickZoom(self):
        self.mainWindow.basePoint = [self.mainWindow.basePoint[0] + self.startX,
                                     self.mainWindow.basePoint[1] + self.startY,
                                     self.endX - self.startX,
                                     self.endY - self.startY]
        image = self.processImage[self.startY:self.endY, self.startX:self.endX]
        self.mainWindow.showImage(image, original=False, isZoomImage=True)

    def clickAddPaintArea(self):
        self.mainWindow.researchingTab.stepSettingFrame.stepParameter.paintArea = (self.mainWindow.basePoint[0] + self.startX,
                                                                                   self.mainWindow.basePoint[1] + self.startY,
                                                                                   self.mainWindow.basePoint[0] + self.endX,
                                                                                   self.mainWindow.basePoint[1] + self.endY)

    def clickAddWorkingArea(self):
        self.mainWindow.researchingTab.stepSettingFrame.stepParameter.workingArea = (self.mainWindow.basePoint[0] + self.startX,
                                                                                     self.mainWindow.basePoint[1] + self.startY,
                                                                                     self.mainWindow.basePoint[0] + self.endX,
                                                                                     self.mainWindow.basePoint[1] + self.endY)
    def clickAddBS_ProcessWorkingArea(self):
        self.mainWindow.researchingTab.stepSettingFrame.stepParameter.bs_processWorkingArea = (self.mainWindow.basePoint[0] + self.startX,
                                                                                               self.mainWindow.basePoint[1] + self.startY,
                                                                                               self.mainWindow.basePoint[0] + self.endX,
                                                                                               self.mainWindow.basePoint[1] + self.endY)

    def clickAddTemplate(self):
        nowTime = TimeControl.y_m_d_H_M_S_format()
        imagePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                          "/",
                                          self.mainWindow.researchingTab.currentAlgorithm.algorithmParameter.name,
                                          "/",
                                          "imageTemplate_",
                                          nowTime,
                                          ".png")
        image = self.processImage[self.startY:self.endY, self.startX:self.endX]
        cv.imencode(".png", image)[1].tofile(imagePath)
        # cv.imwrite(imagePath, image)

        self.mainWindow.researchingTab.stepSettingFrame.stepParameter.templateName = nowTime
    def clickAddRefImage(self):
        nowTime = TimeControl.y_m_d_H_M_S_format()
        imagePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                            "/",
                                            self.mainWindow.researchingTab.currentAlgorithm.algorithmParameter.name,
                                            "/",
                                            "imageReference_",
                                            nowTime,
                                            ".png")
        cv.imencode(".png", self.processImage)[1].tofile(imagePath)
        # cv.imwrite(imagePath, self.processImage)
        self.mainWindow.researchingTab.currentAlgorithm.algorithmParameter.refImageName = nowTime

    def clickAddColorRange(self):
        image = self.processImage[self.startY:self.endY + 1, self.startX:self.endX + 1]
        averageColor = cv.mean(image)

        averageColor = [int(averageColor[0]), int(averageColor[1]), int(averageColor[2])]
        # self.mainWindow.researchingTab.stepSettingFrame.stepParameter.workingArea = (self.startX, self.startY, self.endX, self.endY)
        self.mainWindow.researchingTab.stepSettingFrame.stepParameter.averageColor = averageColor
        # self.mainWindow.researchingTab.stepSettingFrame.showBaseColor()
        self.mainWindow.researchingTab.stepSettingFrame.setAverageColor(averageColor)

