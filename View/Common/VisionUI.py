from tkinter import *
from tkinter import ttk
from CommonAssit import VisionFont, TimeControl
from PIL import Image, ImageTk
from CommonAssit import Color
import enum

class VisionTopLevel(Toplevel):
    def __init__(self, master=None, **kw):
        Toplevel.__init__(self, master=master, bg=Color.visionBg(), **kw)

class VisionFrame(Frame):
    def __init__(self, master, bg=Color.visionBg(), **kw):
        Frame.__init__(self, master=master, bg=bg, **kw)

class VisionSpinBox(Spinbox):
    def __init__(self, master, **kw):
        Spinbox.__init__(self, master, **kw)

class VisionEntry(Entry):
    def __init__(self, master, highlightbackground='green',highlightthickness=1, text=None, **kw):
        Entry.__init__(self, master=master, highlightbackground=highlightbackground, cursor='xterm',
                       highlightthickness=highlightthickness, bd=0, **kw)
        if text is not None:
            self.setValue(text)
    def setValue(self, value):
        self.delete(0, END)
        self.insert(0, f"{value}")

class VisionMenu(Menu):
    def __init__(self, master=None, **kw):
        Menu.__init__(self, master=master, bg=Color.visionBg(), fg=Color.dark_text_color(),
                      activebackground=Color.visionHighlight(), **kw)

class VisionNotebook(ttk.Notebook):
    def __init__(self, master):
        ttk.Notebook.__init__(self, master=master)
        style = ttk.Style()

        style.theme_create("yummy", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": Color.visionBg(), "foreground": Color.dark_text_color()},
                "map": {"background": [("selected", Color.visionHighlight())],
                        "foreground": [("selected", Color.light_text_color())],
                        "expand": [("selected", [1, 1, 1, 0])]}}})

        style.theme_use("yummy")

class VisionLabelFrame(LabelFrame):
    def __init__(self, master,bg=Color.visionBg(), **kw):
        LabelFrame.__init__(self, master=master, bg=bg, fg=Color.dark_text_color(),
                            font=VisionFont.boldFont(10), **kw)
class VisionButton(Button):
    def __init__(self, master, fg=Color.normal_button_fg(), bg=Color.normalButtonBg(),
                 activebackground=Color.active_normal_button_bg(),**kw):
        Button.__init__(self, master=master, bg=bg,
                        activebackground=activebackground,
                        fg=fg, cursor="hand2",
                        highlightthickness=0, **kw)

class VisionLabel(Label):
    def __init__(self, master, bg=Color.visionBg(), fg=Color.dark_text_color(), **kw):
        Label.__init__(self, master=master, bg=bg, fg=fg, **kw)
    def set(self, text=""):
        self.config(text=text)
    def get(self):
        return self['text']

class VisionResultLabel(VisionLabel):
    def __init__(self, master, bg=Color.resultBg(), fg=Color.winWhite(), **kw):
        VisionLabel.__init__(self, master=master, bg=bg, fg=fg, **kw)

class VisionResultNGLabel(VisionLabel):
    def __init__(self, master, bg=Color.resultBg(), fg=Color.winRed(), **kw):
        VisionLabel.__init__(self, master=master, bg=bg, fg=fg, **kw)

class VisionResultOKLabel(VisionLabel):
    def __init__(self, master, bg=Color.resultBg(), fg=Color.winLame(), **kw):
        VisionLabel.__init__(self, master=master, bg=bg, fg=fg, **kw)


class VisionCheckBox(Checkbutton):
    def __init__(self, master, **kw):
        Checkbutton.__init__(self, master=master,
                             bg=Color.visionBg(), **kw, activebackground=Color.visionHighlight())

class VisionMenuButton(Menubutton):
    def __init__(self, master, **kw):
        Menubutton.__init__(self, master=master, bg=Color.visionBg(), activeforeground=Color.light_text_color(),
                            cursor="hand2", justify=CENTER, activebackground=Color.visionHighlight(), **kw)
class OpenButton(Button):
    def __init__(self, master, text="", font=None, command=None):
        Button.__init__(self, master, text=text, command=command, bg="#C1FFC1", fg="#8B0A50", font=font)

class VisionSlider(Scale):
    def __init__(self, master,bg=Color.visionBg(), **kw):
        Scale.__init__(self, master=master, bg=bg,relief=FLAT, cursor="hand2", activebackground='green', **kw)

class ResultLabel(Label):
    def __init__(self, master,  text):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(11), fg=Color.winWhite(), bg=Color.resultBg())

class ResultLabelFrame(LabelFrame):
    def __init__(self, master,  title, **kw):
        LabelFrame.__init__(self, master=master, text=title, font=VisionFont.boldFont(10), bg=Color.resultBg(), fg=Color.winWhite(), **kw)

class ResultFrame(Frame):
    def __init__(self, master, **kw):
        Frame.__init__(self, master=master, bg=Color.resultBg(), **kw)

class ImageButton(Button):
    image = None
    originalImage = None
    def __init__(self, master, image=None, imagePath=None, cursor='hand2', command=None, bg=Color.visionBg(), activebackground=Color.visionBg(), **kw):
        Button.__init__(self, master=master, borderwidth=0, command=command, cursor=cursor,
                        bg=bg, activebackground=activebackground, highlightthickness=0, **kw)
        self.bind("<Configure>", self.onResize)
        if image is not None:
            self.originalImage: Image = image.copy()
            self.showImage()
        if imagePath is not None:
            self.originalImage = Image.open(imagePath)
            self.showImage()

    def onResize(self, event):
        self.showImage()

    def setImage(self, image):
        self.originalImage = image.copy()
        self.showImage()

    def setImagePath(self, imagePath):
        self.originalImage = Image.open(imagePath)
        self.showImage()

    def showImage(self):
        if self.originalImage is None:
            return
        realWidth = self.winfo_width()
        realHeight = self.winfo_height()

        image = self.originalImage.resize((realWidth, realHeight))

        self.image = ImageTk.PhotoImage(image)
        self.config(image=self.image)


class OpenButton1(Button):
    openImage = None
    originalImage = None
    def __init__(self, master, command=None, lblText="", bg=Color.visionBg(), activebackground=Color.visionBg(), font=None):
        self.originalImage = Image.open("./resource/openFolder.png")
        Button.__init__(self, master=master, borderwidth=0,
                        command=command, bg=bg, activebackground=activebackground,
                        text=lblText, font=font,
                        compound=LEFT)

        self.bind("<Configure>", self.onResize)
        self.showImage()

    def onResize(self, event):
        # self.showArrayImage(self.originalImage)
        self.showImage()

    def setImage(self, image):
        self.originalImage = image.copy()
        self.showImage()

    def showImage(self):
        realHeight = int(self.winfo_height() / 2) + 1
        realWidth = realHeight

        image = self.originalImage.resize((realWidth, realHeight))

        self.image = ImageTk.PhotoImage(image)
        self.config(image=self.image)

class SaveButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/save_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class AddButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/add_button.png",command=command,
                             cursor='hand2',bg=bg, activebackground=activebackground)

class DeleteButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/delete_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class CopyButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/copy_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class OkButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/ok_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class CancelButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/cancel_button1.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class StartButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/start_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class TeachingButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/teaching_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class CloseButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self, master=master, imagePath="./resource/close_button.png",
                             cursor='hand2', command=command, bg=bg,
                             activebackground=activebackground)

class ResetButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/reset_button.png",command=command,
                             cursor="hand2", bg=bg, activebackground=activebackground)

class ShowOriginButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/show_origin_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class UpButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/btnUp.png",command=command, bg=bg, activebackground=activebackground)

class DownButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/btnDown.png",command=command, bg=bg, activebackground=activebackground)

class ExecuteButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/execute_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class StartSetupButton(Button):
    def __init__(self, master, text, command=None):
        Button.__init__(self, master=master, bg=Color.resultBg(), fg=Color.winWhite(), font=VisionFont.boldFont(10),
                        cursor="hand2", text=text, command=command, wraplength=126)

class EraseAreaButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/erase_area_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class ShowAreaButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/show_area_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)
class NextButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/next_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class PreviousButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/previous_button.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)

class TakePicButton(ImageButton):
    def __init__(self, master, command=None, bg=Color.visionBg(), activebackground=Color.visionBg()):
        ImageButton.__init__(self,master=master, imagePath="./resource/take_picture.png",command=command,
                             cursor='hand2', bg=bg, activebackground=activebackground)
