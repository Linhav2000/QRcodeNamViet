from View.Common.VisionUI import *
from Modules.ModelSetting.Algorithm_Choose import Algorithm_Choose

class DDK_Algorithm_Choose(Algorithm_Choose):
    step = 0
    plc_pos_btn: VisionButton
    def __init__(self,  master, lblText, yPos, height, valueList, xDistance=100, step=0, selectChangeCommand=None, mainWindow=None, add_new_done_cmd=None):
        Algorithm_Choose.__init__(self,  master, lblText, yPos, height, valueList,
                                  xDistance=xDistance, selectChangeCommand=selectChangeCommand, mainWindow=mainWindow, add_new_done_cmd=None)

        self.step=step
        self.setup_plc_pos_button()

    def setup_plc_pos_button(self):
        self.plc_pos_btn = VisionButton(self, text="PLC Pos", command=self.click_btn_plc_pos)
        self.plc_pos_btn.place(x=self.xDistance + 370, rely=0, width=80, height=23)

    def click_btn_plc_pos(self):
        self.mainWindow.workingThread.create_ddk_inspection()
        self.mainWindow.workingThread.ddk_inspection.request_moving(step=self.step)
