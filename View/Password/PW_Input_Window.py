from View.Common.VisionUI import *
from CommonAssit.FileManager import *
from tkinter import messagebox

class PW_Input_Window(VisionTopLevel):

    passEntry: VisionEntry
    okBtn: OkButton
    label: VisionLabel
    pw = ""
    default_pass = "Mes2021"
    passed = False

    def __init__(self, mainWindow):
        VisionTopLevel.__init__(self)
        self.bind("<Return>", self.push_enter)
        self.mainWindow = mainWindow
        self.setupWindow()
        self.setupView()

    def setupWindow(self):
        width = 436
        height = 250
        # self.protocol("WM_DELETE_WINDOW", self.click_btn_ok)
        self.title("Password")
        self.iconbitmap('resource\\appIcon.ico')
        self.geometry("{}x{}+{}+{}".format(width, height, int (self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - width / 2),
                                           int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - height / 2)))
        self.resizable(0, 0)
        self.grab_set()

    def setupView(self):
        self.label = VisionLabel(self, text="Please enter password to access!")
        self.label.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.3)

        self.passEntry = VisionEntry(self, show="*")
        self.passEntry.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.12)
        self.passEntry.focus_set()

        self.okBtn = OkButton(self, command=self.click_btn_ok)
        self.okBtn.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.2)

    def push_enter(self, event=None):
        self.click_btn_ok()

    def click_btn_ok(self):
        if self.checkPassword(self.passEntry.get()):
            self.passed = True
            self.destroy()
        else:
            messagebox.showwarning("Password", "Wrong password!")

    def checkPassword(self, pw):
        pw_file_path = "./resource/pw.txt"
        pw_file = TextFile(pw_file_path)
        if len(pw_file.readFile()) < 1:
            pw_file.dataList = [self.default_pass]
            pw_file.saveFile()
            if pw == self.default_pass:
                return  True
        elif pw_file.dataList[0] == pw:
            return True
        else:
            return False