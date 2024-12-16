from View.Common.VisionUI import *

class DDK_Result_Parameter:
    current_station = 0
    current_step = 0
    step_passed = False
    step_process_time = 0
    product_passed = True
    product_process_time = 0
    total = 0
    total_passed = 0
    total_NG = 0


class DDK_Result_Frame(VisionLabelFrame):

    height = 30
    title_align = 300

    current_station_title: VisionResultLabel
    current_station: VisionResultLabel
    current_step_title: VisionResultLabel
    current_step: VisionResultLabel
    step_process_time_title: VisionResultLabel
    step_process_time: VisionResultLabel
    product_process_time_title: VisionResultLabel
    product_process_time: VisionResultLabel
    total_passed_title: VisionResultOKLabel
    total_passed: VisionResultOKLabel
    total_NG_title: VisionResultNGLabel
    total_NG: VisionResultNGLabel
    total_title: VisionResultLabel
    total: VisionResultLabel
    btn_reset_process: VisionButton

    def __init__(self, master, mainWindow):
        self.mainWindow=mainWindow
        VisionLabelFrame.__init__(self, master, text=self.mainWindow.languageManager.localized("ddkResult"), bg=Color.resultBg())
        self.setupView()
        self.notifyRegister()

    def notifyRegister(self):
        self.mainWindow.notificationCenter.add_observer(with_block=self.changeLanguage, for_name="ChangeLanguage")

    def changeLanguage(self, sender, notification_name, info):
        self.current_station_title.config(text=self.mainWindow.languageManager.localized("currentStation"))
        self.current_step_title.config(text=self.mainWindow.languageManager.localized("currentStep"))
        self.step_result_title.config(text=self.mainWindow.languageManager.localized("stepResult"))
        self.step_process_time_title.config(text=self.mainWindow.languageManager.localized("stepTactTime"))
        self.product_process_time_title.config(text=self.mainWindow.languageManager.localized("productTactTime"))
        self.total_passed_title.config(text=self.mainWindow.languageManager.localized("totalOkProduct"))
        self.total_NG_title.config(text=self.mainWindow.languageManager.localized("totalNGProduct"))
        self.total_title.config(text=self.mainWindow.languageManager.localized("totalProduct"))

    def setupView(self):
        self.current_station_title = VisionResultLabel(self, text=self.mainWindow.languageManager.localized("currentStation"),
                                                       font=VisionFont.boldFont(12))
        self.current_station_title.place(x=5, y=0*self.height + 5, height=self.height)
        self.current_station = VisionResultLabel(self, text="0", font=VisionFont.boldFont(12))
        self.current_station.place(x=5+self.title_align, y=0*self.height + 5, height=self.height)

        self.current_step_title = VisionResultLabel(self, text=self.mainWindow.languageManager.localized("currentStep"),
                                                    font=VisionFont.boldFont(12))
        self.current_step_title.place(x=5, y=1*self.height + 5, height=self.height)
        self.current_step = VisionResultLabel(self, text="0", font=VisionFont.boldFont(12))
        self.current_step.place(x=5+self.title_align, y=1*self.height + 5, height=self.height)

        self.step_result_title = VisionResultLabel(self, text=self.mainWindow.languageManager.localized("stepResult"),
                                                   font=VisionFont.boldFont(12))
        self.step_result_title.place(x=5, y=2*self.height + 5, height=self.height)
        self.step_result_ok = VisionResultOKLabel(self, text="OK", font=VisionFont.boldFont(12))
        self.step_result_ng = VisionResultNGLabel(self, text="NG", font=VisionFont.boldFont(12))
        self.step_result_ok.place(x=5 + self.title_align, y=2 * self.height + 5, height=self.height)

        self.step_process_time_title = VisionResultLabel(self, text=self.mainWindow.languageManager.localized("stepTactTime"),
                                                         font=VisionFont.boldFont(12))
        self.step_process_time_title.place(x=5, y=3*self.height + 5, height=self.height)
        self.step_process_time = VisionResultLabel(self, text="0s", font=VisionFont.boldFont(12))
        self.step_process_time.place(x=5+self.title_align, y=3*self.height + 5, height=self.height)

        self.product_process_time_title = VisionResultLabel(self, text=self.mainWindow.languageManager.localized("productTactTime"),
                                                            font=VisionFont.boldFont(12))
        self.product_process_time_title.place(x=5, y=4*self.height + 5, height=self.height)
        self.product_process_time = VisionResultLabel(self, text="0s", font=VisionFont.boldFont(12))
        self.product_process_time.place(x=5+self.title_align, y=4*self.height + 5, height=self.height)


        self.total_passed_title = VisionResultOKLabel(self, text=self.mainWindow.languageManager.localized("totalOkProduct"),
                                                      font=VisionFont.boldFont(12))
        self.total_passed_title.place(x=5, y=5*self.height + 5, height=self.height)
        self.total_passed = VisionResultOKLabel(self, text="0", font=VisionFont.boldFont(12))
        self.total_passed.place(x=5+self.title_align, y=5*self.height + 5, height=self.height)

        self.total_NG_title = VisionResultNGLabel(self, text=self.mainWindow.languageManager.localized("totalNGProduct"),
                                                  font=VisionFont.boldFont(12))
        self.total_NG_title.place(x=5, y=6*self.height + 5, height=self.height)
        self.total_NG = VisionResultNGLabel(self, text="0", font=VisionFont.boldFont(12))
        self.total_NG.place(x=5+self.title_align, y=6*self.height + 5, height=self.height)


        self.total_title = VisionResultLabel(self, text=self.mainWindow.languageManager.localized("totalProduct"),
                                             font=VisionFont.boldFont(12))
        self.total_title.place(x=5, y=7*self.height + 5, height=self.height)
        self.total = VisionResultLabel(self, text="0", font=VisionFont.boldFont(12))
        self.total.place(x=5+self.title_align, y=7*self.height + 5, height=self.height)

        self.btn_reset_process = VisionButton(self, text="Reset Process", font=VisionFont.boldFont(12), command=self.click_btn_reset_process)
        self.btn_reset_process.place(relx=0.05, rely=0.9, relwidth=0.3, relheight=0.08)

    def click_btn_reset_process(self):
        if self.mainWindow.workingThread.ddk_inspection is not None:
            self.mainWindow.workingThread.ddk_inspection.request_reset()

    def setValue(self, ddk_result: DDK_Result_Parameter):
        self.current_station.set(ddk_result.current_station)
        self.current_step.set(ddk_result.current_step)
        self.step_process_time.set(ddk_result.step_process_time)
        self.product_process_time.set(ddk_result.product_process_time)
        self.total_passed.set(ddk_result.total_passed)
        self.total_NG.set(ddk_result.total_NG)
        self.total.set(ddk_result.total)

        if ddk_result.step_passed:
            self.step_result_ok.place(x=5 + self.title_align, y=2 * self.height + 5, height=self.height)
            self.step_result_ng.place_forget()
        else:
            self.step_result_ok.place_forget()
            self.step_result_ng.place(x=5 + self.title_align, y=2 * self.height + 5, height=self.height)