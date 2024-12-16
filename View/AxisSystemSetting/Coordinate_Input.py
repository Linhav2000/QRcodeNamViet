from View.Common.VisionUI import *


class Coordinate_Input(VisionFrame):

    x_coordinate: VisionLabel
    y_coordinate: VisionLabel

    def __init__(self, master, label, yPos, height, rel_width=1):
        VisionFrame.__init__(self, master=master)
        self.label = label
        self.setupView()
        self.place(x=0, y=yPos, relwidth=rel_width, height=height)

    def setupView(self):
        label = VisionLabel(self, text=self.label)
        label.place(relx=0, rely=0,relheight=1)

        self.x_coordinate = VisionLabel(self, bg="white", highlightbackground='green',highlightthickness=1)
        self.x_coordinate.place(relx=0.4, rely=0.1, relwidth=0.25, relheight=0.8)

        self.y_coordinate = VisionLabel(self, bg="white", highlightbackground='green',highlightthickness=1)
        self.y_coordinate.place(relx=0.73, rely=0.1, relwidth=0.25, relheight=0.8)

    def setValue(self, coors):
        self.x_coordinate.set(coors[0])
        self.y_coordinate.set(coors[1])

    def getIntValue(self):
        try:
            return int(float(self.x_coordinate.get())), int(float(self.y_coordinate.get()))
        except None:
            return 0, 0

    def getFloatValue(self):
        try:
            return float(self.x_coordinate.get()), float(self.y_coordinate.get())
        except None:
            return 0, 0
