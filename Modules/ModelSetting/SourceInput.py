from View.Common.VisionUI import *
from ImageProcess.Algorithm.AlgorithmResult import AlgorithmResultKey

class SourceInput(VisionFrame):
    label: VisionLabel
    maxStep = 99
    stepValueList = []
    paramValueList = []
    xDistance = 120
    stepCombo: ttk.Combobox
    paramNameCombo: ttk.Combobox
    btnShow: VisionButton
    showCommand: None

    def __init__(self, master, lblText, maxStep, yPos, height, xDistance=100,
                 combo_width=100, sourceImageName=None, showCommand=None):
        VisionFrame.__init__(self, master)
        self.lblText = lblText
        self.yPos = yPos
        self.xDistance = xDistance
        self.combo_width = combo_width
        self.showCommand = showCommand
        self.maxStep = maxStep
        self.initValue()
        self.setupView()
        self.sourceImageName = sourceImageName
        self.place(x=0, y=yPos, relwidth=1, height=height)

    def initValue(self):
        self.stepValueList = []
        self.paramValueList = []

        for name, member in AlgorithmResultKey.__members__.items():
            self.paramValueList.append(name)

        self.stepValueList = []
        self.stepValueList.append("Reference Image")
        self.stepValueList.append("Template")
        self.stepValueList.append("None")
        self.stepValueList.append("Original Image")
        for i in range(self.maxStep):
            self.stepValueList.append("Step {}".format(i))

    def setupView(self):
        label = VisionLabel(self, text=self.lblText)
        label.place(x=5, y=0)

        self.stepCombo = ttk.Combobox(self, state="readonly", value=self.stepValueList, cursor="hand2")
        self.stepCombo.place(x=self.xDistance, y=0, width=self.combo_width, height=20)

        self.paramNameCombo = ttk.Combobox(self, state="readonly", value=self.paramValueList, cursor="hand2")
        self.paramNameCombo.place(x=self.xDistance + self.combo_width + 10, y=0, width=self.combo_width, height=20)

        self.btnShow = VisionButton(self, text="Show", command=self.clickBtnShow)
        self.btnShow.place(x=self.xDistance + 2*self.xDistance + 20, y=0, width=80, height=25)

    def clickBtnShow(self):
        if self.showCommand is not None:
            self.showCommand(self.getValue(), self.sourceImageName)

    def getValue(self):
        stepPos = self.stepCombo.current() - 4

        paramName = ""
        for name, member in AlgorithmResultKey.__members__.items():
            if name == self.paramNameCombo.get():
                paramName = member.value
                break

        return stepPos, paramName

    def setValue(self, value):
        try:
            stepPos, paramName = value
            self.stepCombo.current(stepPos + 4)

            for name, member in AlgorithmResultKey.__members__.items():
                if member.value == paramName:
                    self.paramNameCombo.current(self.paramValueList.index(name))
                    break

        except:
            pass

