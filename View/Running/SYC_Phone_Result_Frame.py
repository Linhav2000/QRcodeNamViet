from View.Password.PW_Input_Window import PW_Input_Window
from View.Common.VisionUI import *
from CommonAssit import PathFileControl
from CommonAssit.FileManager import *
import jsonpickle

class SYC_Phone_Result_Parameter:
    total = 0
    total_NG = 0
    total_OK = 0
class SYC_Phone_Result_Frame(VisionFrame):
    pass_word = PW_Input_Window
    height = 30
    title_align = 170
    btnResetProcess : ImageButton
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
    syc_current_result_OK: VisionResultLabel
    total_OK: VisionResultOKLabel
    syc_current_result_NG: Label
    process_result_frame: LabelFrame
    dataFilePath = "./data/Phone Check/ok_ng_process.json"
    def __init__(self, master, mainWindow):
        VisionFrame.__init__(self, master, bg=Color.resultBg())
        self.mainWindow=mainWindow
        self.syc_result_parameter = SYC_Phone_Result_Parameter()
        self.loadParameter()

        self.setupView()

    def loadParameter(self):
        dataPath = "./data"
        phone_check_folder = f"{dataPath}/Phone Check"
        parameter_file_path = f"{phone_check_folder}/ok_ng_process.json"

        # PathFileControl.generatePath(dataPath)
        PathFileControl.generatePath(phone_check_folder)
        try:
            file = JsonFile(parameter_file_path)
            jsonData = file.readFile()
            self.syc_result_parameter = jsonpickle.decode(jsonData)
        except Exception as error:
            try:
                self.mainWindow.runningTab.insertLog("ERROR Get common setting: {}".format(error))
            except:
                pass

    def saveParameter(self):
        try:
            file = JsonFile(self.dataFilePath)
            jsonData = jsonpickle.encode(self.syc_result_parameter)
            file.data = jsonData
            file.saveFile()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Common setting: {}".format(error))

    def setupView(self):
        self.syc_current_result_NG = Label(self, text="NG", bg=Color.resultBg(), fg=Color.winRed(),
                                                          font=VisionFont.boldFont(120))
        self.syc_current_result_OK = VisionResultLabel(self,text="Hello!", bg=Color.resultBg(),
                                                       fg=Color.winLame(), font=VisionFont.boldFont(120))
        self.syc_current_result_OK.place(relx=0, rely=0.05, relwidth=1, relheight=0.52)

        self.process_result_frame = LabelFrame(self,text="Progress result:", bg=Color.resultBg(),
                                               font=VisionFont.boldFont(10), fg=Color.winWhite())
        self.process_result_frame.place(relx=0 , rely=0.58, relwidth=1, relheight=0.42)

        self.total_OK = VisionResultOKLabel(self.process_result_frame, text="Total OK product : ",
                                            fg=Color.winBlue(), font=VisionFont.boldFont(12))
        self.total_OK.place(x=5, y=0.1*self.height + 15, height=self.height)
        self.total_OK = VisionResultOKLabel(self.process_result_frame, text=self.syc_result_parameter.total_OK,fg=Color.winBlue(),
                                            font=VisionFont.boldFont(12))
        self.total_OK.place(x=0.5+self.title_align, y=0.1*self.height + 15, height=self.height)

        self.total_NG_title = VisionResultNGLabel(self.process_result_frame, text="Total NG product : ",fg=Color.winYellow(), font=VisionFont.boldFont(12))
        self.total_NG_title.place(x=5, y=1*self.height + 20, height=self.height)
        self.total_NG = VisionResultNGLabel(self.process_result_frame, text=self.syc_result_parameter.total_NG,fg=Color.winYellow(), font=VisionFont.boldFont(12))
        self.total_NG.place(x=0.5+self.title_align, y=1*self.height + 20, height=self.height)


        self.total_title = VisionResultLabel(self.process_result_frame, text="Total product  : ", font=VisionFont.boldFont(12))
        self.total_title.place(x=5, y=2.3*self.height + 10, height=self.height)
        self.total = VisionResultLabel(self.process_result_frame, text=self.syc_result_parameter.total, font=VisionFont.boldFont(12))
        self.total.place(x=0.5+self.title_align, y=2.3*self.height + 10, height=self.height)


        self.btn_reset_process = VisionButton(self.process_result_frame, text="Reset Process", font=VisionFont.boldFont(12),
                                              command=self.click_btn_reset_process)
        self.btn_reset_process.place(relx=0.65, rely=0.28, relwidth=0.3, relheight=0.6)
        # self.btnResetProcess = ImageButton(self,imagePath="./resource/8.png",command=self.click_btn_reset_process)
        # self.btnResetProcess.place(relx=0.65, rely=0.7, relwidth=0.3, relheight=0.25)
    def click_btn_reset_process(self):
        password_window = PW_Input_Window(self.mainWindow)
        password_window.wait_window()
        if password_window.passed:
            self.syc_result_parameter.total_OK = 0
            self.syc_result_parameter.total_NG = 0
            self.syc_result_parameter.total = 0
            self.saveParameter()

            self.total_OK.set("0")
            self.total_NG.set("0")
            self.total.set("0")

    def update_value(self, parameter: SYC_Phone_Result_Parameter):
        self.syc_result_parameter = parameter
        self.syc_result_parameter.total = self.syc_result_parameter.total_OK + self.syc_result_parameter.total_NG
        self.total_NG.set(parameter.total_NG)
        self.total_OK.set(parameter.total_OK)
        self.total.set(parameter.total)
        self.saveParameter()

    def update_label_ok(self):
        self.syc_current_result_NG.place_forget()
        self.syc_current_result_OK.set("OK")
        self.syc_current_result_OK.place(relx=0, rely=0.05, relwidth=1, relheight=0.52)

    def update_label_ng(self):
        self.syc_current_result_OK.place_forget()
        self.syc_current_result_NG.place(relx=0, rely=0.05, relwidth=1, relheight=0.52)
