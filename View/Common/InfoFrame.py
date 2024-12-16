from View.Common.VisionUI import *

class InfoFrame(ResultFrame):
    title = ""
    value = ""
    valueLabel: ResultLabel

    def __init__(self, master, title, value=""):
        ResultFrame.__init__(self, master=master)
        self.title = title
        self.value = value
        self.setupView()

    def setupView(self):
        label = ResultLabel(self, text=self.title)
        label.place(relx=0.01, rely=0, relheight=1)

        self.valueLabel = ResultLabel(self, text=self.value)
        self.valueLabel.place(relx=0.5, rely=0, relheight=1)

    def setValue(self, value):
        self.valueLabel.config(text="{}".format(value))