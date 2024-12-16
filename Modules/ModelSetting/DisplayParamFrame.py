from View.Common.VisionUI import *

class DisplayParamFrame(VisionFrame):
    label: VisionLabel
    disPlayLabel: Label
    # parameterEntry: Entry
    xDistance = 150

    def __init__(self, master, lblText, yPos, height):
        VisionFrame.__init__(self, master)
        self.lblText = lblText
        self.yPos = yPos
        self.setupView()
        self.place(x=0, y=yPos, relwidth=1, height=height)

    def setupView(self):
        label = VisionLabel(self, text=self.lblText)
        label.place(x=5, y=0)
        self.disPlayLabel = Label(self, bg='white')
        self.disPlayLabel.place(x=self.xDistance, y=0, width= 150, height=20)

    def getValue(self):
        return self.disPlayLabel['text']

    def getIntValue(self):
        try:
            return int(float(self.disPlayLabel['text']))
        except:
            return 0

    def getFloatValue(self):
        try:
            return float(self.disPlayLabel['text'])
        except:
            return 0.0

    def setValue(self, value):
        self.disPlayLabel.config(text="{}".format(value))
