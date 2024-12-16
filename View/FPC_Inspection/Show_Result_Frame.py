from View.Common.VisionUI import *
from CommonAssit import VisionFont
class Show_Result_Frame(VisionLabelFrame):
    label: VisionLabel
    value: VisionLabel
    color = "#00FF00"
    text = ""
    def __init__(self, master, color="#00FF00", text="OK"):
        VisionLabelFrame.__init__(self, master=master, bd=5)
        self.color = color
        self.text = text
        self.setupView()
    def setupView(self):
        self.label = VisionLabel(self, text=self.text, fg=self.color, font=VisionFont.boldFont(18))
        self.label.place(relx=0, rely=0, relwidth=1, relheight=0.5)
        self.value = VisionLabel(self, text="Value", fg=self.color, font=VisionFont.boldFont(18))
        self.value.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

    def setValue(self, value):
        self.value.config(text=f"{value}")