from View.Common.VisionUI import *
from View.Common.RangeSlider import RangeSlider
from tkinter import filedialog

class ComboxBoxStepParmFrame(VisionFrame):
    label: VisionLabel
    comboBox: ttk.Combobox
    valueList = []
    xDistance = 150


    def __init__(self, master, lblText, yPos, height,codeList, valueList=None):

        VisionFrame.__init__(self, master)
        self.codeList = codeList
        self.lblText = lblText
        self.yPos = yPos
        self.valueList = valueList
        self.setupView()
        self.place(x=0, y=yPos, relwidth=1, height=height)

    def setupView(self):
        self.label = VisionLabel(self, text=self.lblText)
        self.label.place(x=5, y=0)
        self.comboBox = ttk.Combobox(self, state="readonly", value=self.valueList, cursor="hand2")
        self.comboBox.place(x=self.xDistance, y=0, width=150, height=20)

    def update_Language(self, new_text):
        self.label.config(text=new_text)

    def getValue(self):
        ret = None
        for name, member in self.codeList.__members__.items():
            if name == self.comboBox.get():
                ret = member.value
                break
        return ret

    def getPosValue(self):
        try:
            return self.comboBox.current()
        except:
            return 0

    def setPosValue(self, value):
        try:
            self.comboBox.current(value)
        except:
            pass

    def setStringValue(self, value):
        for name, member in self.codeList.__members__.items():
            if member.value == value:
                self.comboBox.current(self.valueList.index(name))
                break
class Range_Input(VisionFrame):
    label: VisionLabel
    xDistance = 150
    range_slider: RangeSlider
    minRange: VisionSpinBox
    maxRange: VisionSpinBox
    slider_just_change_flag = False
    spin_box_just_change_flag = False
    def __init__(self, master, lblText, yPos, height, width=50,
                 minValue=0, maxValue=255, resolution=1,
                 button_up_cmd=None, change_val_cmd=None):
        VisionFrame.__init__(self, master=master)

        self.minRange_string_var = StringVar(self)
        self.maxRange_string_var = StringVar(self)
        self.lblText = lblText
        self.yPos = yPos
        self.height = height
        self.width = width
        self.minValue = minValue
        self.maxValue = maxValue
        self.button_up_cmd = button_up_cmd
        self.change_val_cmd = change_val_cmd
        self.resolution = resolution

        self.setupView()
        self.place(x=0, y=yPos, relwidth=1, height=height)

    def setupView(self):
        self.label = VisionLabel(self, text=self.lblText)
        self.label.place(x=5, rely=0, relheight=1)

        self.minRange = VisionSpinBox(self,from_=self.minValue, to=self.maxValue,
                                           textvariable=self.minRange_string_var)
        self.minRange.bind("<ButtonRelease-1>", self.boxSpin_button_release)
        self.minRange_string_var.trace('w', self.boxSpin_input_text)
        self.minRange.place(x=self.xDistance, rely=0.1, width=self.width, relheight=0.8)


        self.range_slider = RangeSlider(self, width=200, height=self.height,
                                        min_val=self.minValue, max_val=self.maxValue, show_value=False,
                                        init_lis=[self.minValue, self.maxValue],
                                        button_up_cmd=self.rangeSlider_button_up,
                                        change_value_cmd=self.rangeSlider_change_value,
                                        bg=Color.visionBg())
        self.range_slider.place(x=self.xDistance + self.width + 5, y = 0, width=200, height=self.height)

        self.maxRange = VisionSpinBox(self, from_=self.minValue, to=self.maxValue,
                                      textvariable=self.maxRange_string_var)
        self.maxRange.bind("<ButtonRelease-1>", self.boxSpin_button_release)
        self.maxRange_string_var.trace('w', self.boxSpin_input_text)
        self.maxRange.place(x=self.xDistance + self.width + 5 + 200 + 5, rely=0.1, width=self.width, relheight=0.8)

    def update_Language(self, new_text):
        self.label.config(text=new_text)

    def rangeSlider_change_value(self, values):
        self.slider_just_change_flag = True
        if values[0] != self.minRange_string_var.get():
            self.minRange_string_var.set(values[0])
        if values[1] != self.maxRange_string_var.get():
            self.maxRange_string_var.set(values[1])

    def rangeSlider_button_up(self, values):
        if self.button_up_cmd is not None:
            self.button_up_cmd(self.range_slider.getValues())

    def boxSpin_input_text(self, name='', index='', mode=''):
        try:
            if self.range_slider.getValues() != (float(self.minRange.get()), float(self.maxRange.get())):
                self.range_slider.setValue((float(self.minRange.get()), float(self.maxRange.get())))
        except:
            pass

    def boxSpin_button_release(self, event):
        if self.button_up_cmd is not None:
            self.button_up_cmd(self.range_slider.getValues())

    # def spinbox_change_value(self):
    #     self.spin_box_just_change_flag = True
    #     if not self.slider_just_change_flag:
    #         self.range_slider.setValue((float(self.minRange.get()), float(self.maxRange.get())))
    #     self.slider_just_change_flag = False

    def setValue(self, range_values):
        try:
            # self.range_slider.setValue(range_values)
            self.minRange_string_var.set(range_values[0])
            self.maxRange_string_var.set(range_values[1])

            self.minRange_string_var.set(range_values[0])
            self.maxRange_string_var.set(range_values[1])
        except:
            pass

    def getValue(self):
        return self.range_slider.getValues()

class Slider_Input_Frame(VisionFrame):
    label: VisionLabel
    xDistance = 100
    slider: VisionSlider
    buttonUP: VisionButton
    buttonDown: VisionButton
    # inputEntry: VisionEntry
    spinBox_input: VisionSpinBox
    currentVal = 0
    change_spinbox_flag = True

    first_set = True
    def __init__(self, master, lblText, yPos, height, width=50,
                 minValue=0, maxValue=255, resolution=1,
                 button_up_cmd=None, change_val_cmd=None):
        VisionFrame.__init__(self, master)
        self.entryString = StringVar(self)
        self.input_boxSpin_string = StringVar(self)
        self.lblText = lblText
        self.yPos = yPos
        self.width = width
        self.minValue = minValue
        self.maxValue = maxValue
        self.button_up_cmd = button_up_cmd
        self.change_val_cmd = change_val_cmd
        self.resolution = resolution
        self.setupView()
        self.place(x=0, y=yPos, relwidth=1, height=height)

    def setupView(self):
        self.label = VisionLabel(self, text=self.lblText)
        self.label.place(x=5, y=0)
        # self.inputEntry = VisionEntry(self, textvariabl=self.entryString)
        # self.entryString.trace('w', self.when_input_entry)
        # self.inputEntry.place(x=self.xDistance, y=0, width=self.width, height=20)

        self.slider = VisionSlider(self, orient=HORIZONTAL, state=NORMAL, bd=0, highlightbackground='green',
                                   from_=self.minValue, to=self.maxValue, showvalue=0,
                                   command=self.whenSliderChangeValue, resolution=self.resolution)
        self.slider.bind("<ButtonRelease-1>", self.slider_button_up)
        self.slider.place(x=self.xDistance +self.width + 10 + 25 + 5, y=0, width=200)

        self.buttonDown = VisionButton(self, text = "<<", command=self.btn_down_click, font=VisionFont.boldFont(10))
        self.buttonDown.place(x=self.xDistance +self.width + 10, y=0, width=25, height=20)

        self.buttonUP = VisionButton(self, text=">>", command=self.btn_up_click, font=VisionFont.boldFont(10))
        self.buttonUP.place(x=self.xDistance + self.width + 10 + 25 + 5 + 200 + 5, y=0, width=25, height=20)

        self.spinBox_input = VisionSpinBox(self,from_=self.minValue, to=self.maxValue,
                                           textvariable=self.input_boxSpin_string, command=self.spinbox_change_value)
        self.spinBox_input.bind("<ButtonRelease-1>", self.boxSpin_button_release)
        self.input_boxSpin_string.trace('w', self.boxSpin_input_text)

        self.spinBox_input.place(x=self.xDistance, y=0, width=self.width, height=20)

    def update_Language(self, new_text):
        self.label.config(text=new_text)

    def spinbox_change_value(self):
        try:
            self.slider.set(float(self.spinBox_input.get()))
        except:
            pass

    def boxSpin_input_text(self, name='', index='', mode=''):

        try:
            if not self.first_set:
                self.slider.set(float(self.spinBox_input.get()))
            self.first_set = False
        except:
            pass

    def boxSpin_button_release(self, event):
        if self.button_up_cmd is not None:
            self.button_up_cmd(self.slider.get())

    def setValue(self, value):
        self.currentVal = value
        self.slider.set(value)

    def getValue(self):
        return int(float(self.slider.get()))

    def getIntValue(self):
        return int(float(self.slider.get()))

    def getFloatValue(self):
        return float(self.slider.get())

    def btn_up_click(self):
        if self.currentVal == self.maxValue:
            return
        self.currentVal += self.resolution
        self.slider.set(self.currentVal)
        if self.button_up_cmd is not None:
            self.button_up_cmd(self.slider.get())

    def btn_down_click(self):
        if self.currentVal == self.minValue:
            return
        self.currentVal -= self.resolution
        self.slider.set(self.currentVal)
        if self.button_up_cmd is not None:
            self.button_up_cmd(self.slider.get())

    def whenSliderChangeValue(self, val):
        self.currentVal = float(val)
        self.input_boxSpin_string.set(self.currentVal)
        if self.change_val_cmd is not None:
            self.change_val_cmd(float(val))

    def slider_button_up(self, event):
        if self.button_up_cmd is not None:
            self.button_up_cmd(float(self.slider.get()))

class InputParamFrame(VisionFrame):
    label: VisionLabel
    parameterEntry: VisionEntry
    xDistance = 150

    def __init__(self, master, lblText, yPos, height, width=50):
        VisionFrame.__init__(self, master)
        self.lblText = lblText
        self.yPos = yPos
        self.width = width
        self.setupView()
        self.place(x=0, y=yPos, relwidth=1, height=height)

    def setupView(self):
        self.label = VisionLabel(self, text=self.lblText)
        self.label.place(x=5, y=0)

        self.parameterEntry = VisionEntry(self)
        self.parameterEntry.place(x=self.xDistance, y=0, width= self.width, height=20)

    def update_Language(self, new_text):
        self.label.config(text=new_text)

    def getValue(self):
        return self.parameterEntry.get()

    def getIntValue(self):
        try:
            return int(float(self.parameterEntry.get()))
        except:
            return 0

    def getFloatValue(self):
        try:
            return float(self.parameterEntry.get())
        except:
            return 0.0

    def setValue(self, value):
        self.parameterEntry.delete(0, END)
        self.parameterEntry.insert(0, "{}".format(value))
        self.parameterEntry.xview("end")

class SaveImageOption(VisionFrame):
    label: VisionLabel
    checked: VisionCheckBox
    save_image_type: ttk.Combobox
    choose_path_btn: VisionButton
    path_entry: VisionEntry
    chosenVar: BooleanVar
    image_save_types = []
    image_draw_types = []
    image_draw: ttk.Combobox

    def __init__(self, master, text, yPos, height):
        VisionFrame.__init__(self, master=master)
        self.text = text
        self.setupView()
        self.place(x=0, y=yPos, relwidth=1, height=height)


    def setupView(self):
        self.label = VisionLabel(self, text=self.text)
        self.label.place(x=5, y=0)

        self.chosenVar = BooleanVar()
        self.checked = VisionCheckBox(self, variable=self.chosenVar)
        self.checked.place(relx=0.2, rely=0, relwidth=0.06, relheight=1)

        self.image_save_types = ["jpg", "png", "bmp"]
        self.save_image_type = ttk.Combobox(self, values=self.image_save_types)
        self.save_image_type.place(relx=0.28, rely=0.15, relwidth=0.1, relheight=0.7)

        self.image_draw_types = ["None", "Draw"]
        self.image_draw = ttk.Combobox(self, values=self.image_draw_types)
        self.image_draw.place(relx=0.4, rely=0.15, relwidth=0.1, relheight=0.7)

        self.path_entry = VisionEntry(self)
        self.path_entry.place(relx=0.52, rely=0.1, relwidth=0.24, relheight=0.8)

        self.choose_path_btn = VisionButton(self, text="Select", command=self.click_btn_choose_path)
        self.choose_path_btn.place(relx=0.78, rely=0.1, relwidth=0.2, relheight=0.8)

    def update_Language(self, new_text):
        self.label.config(text=new_text)

    def setValue(self, save_info):
        try:
            self.chosenVar.set(save_info[0])
            self.save_image_type.current(self.image_save_types.index(save_info[1]))
            self.path_entry.setValue(save_info[2])
            self.image_draw.current(self.image_draw_types.index(save_info[3]))
        except:
            self.chosenVar.set(False)
            self.save_image_type.set("")
            self.image_draw.set("")
            self.path_entry.setValue("")
            pass

    def getValue(self):
        return self.chosenVar.get(), self.save_image_type.get(), self.path_entry.get(), self.image_draw.get()

    def click_btn_choose_path(self):
        saveFolder = filedialog.askdirectory(title="Select Cut Image Dir", initialdir=self.path_entry.get())
        if saveFolder == "":
            return
        self.path_entry.setValue(saveFolder)

class IgnoreArea(VisionFrame):
    label: VisionLabel
    btnShow: VisionButton
    btnDelete: VisionButton
    xDistance = 120
    delete_cmd = None
    show_cmd = None
    area = (0, 0, 0, 0)

    def __init__(self, master, area_id, yPos, height, area, show_cmd=None, delete_cmd = None):
        VisionFrame.__init__(self, master)
        self.area_id = area_id
        self.area = area
        self.show_cmd = show_cmd
        self.delete_cmd = delete_cmd
        self.setupView()
        self.place(x=0, y=yPos, relwidth=1, height=height)

    def setupView(self):
        self.label = VisionLabel(self, text=f"Area {self.area_id + 1}")
        self.label.place(x=5, y=0)
        deleteText = "Delete"
        showText = "Show"
        self.btnShow = VisionButton(self, text=showText, command=self.click_btn_show)
        self.btnShow.place(x=self.xDistance, y=0, width=80, height=25)
        self.btnDelete = VisionButton(self, text=deleteText, command=self.click_btn_delete)
        self.btnDelete.place(x=self.xDistance + 100, y=0, width=80, height=25)

    def update_Language(self, new_text):
        self.label.config(text=f"{new_text} {self.area_id + 1}")

    def click_btn_show(self):
        if self.show_cmd is not None:
            self.show_cmd(self.area[0], self.area[1], self.area_id)

    def click_btn_delete(self):
        if self.delete_cmd is not None:
            self.delete_cmd(self.area_id)

    def getValue(self):
        return self.area

class Coordinate_Input(VisionFrame):
    label: VisionLabel
    x_coordinate: VisionEntry
    y_coordinate: VisionEntry

    def __init__(self, master, label, yPos, height, rel_width=1):
        VisionFrame.__init__(self, master=master)
        self.label_text = label
        self.setupView()
        self.place(x=0, y=yPos, relwidth=rel_width, height=height)

    def setupView(self):
        self.label = VisionLabel(self, text=self.label_text)
        self.label.place(relx=0, rely=0,relheight=1)

        self.x_coordinate = VisionEntry(self, bg="white", highlightbackground='green',highlightthickness=1)
        self.x_coordinate.place(relx=0.4, rely=0.1, relwidth=0.25, relheight=0.8)

        self.y_coordinate = VisionEntry(self, bg="white", highlightbackground='green',highlightthickness=1)
        self.y_coordinate.place(relx=0.73, rely=0.1, relwidth=0.25, relheight=0.8)

    def update_Language(self, new_text):
        self.label.config(text=new_text)

    def setValue(self, coors):
        self.x_coordinate.setValue(coors[0])
        self.y_coordinate.setValue(coors[1])

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
        self.label = VisionLabel(self, text=self.lblText)
        self.label.place(x=5, y=0)
        self.disPlayLabel = Label(self, bg='white')
        self.disPlayLabel.place(x=self.xDistance, y=0, width= 150, height=20)

    def update_Language(self, new_text):
        self.label.config(text=new_text)

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

class CheckboxStepParamFrame(VisionFrame):
    label: VisionLabel
    parameterCheckbox: VisionCheckBox
    chosenVar: BooleanVar
    xDistance = 180
    command=None
    check_box_label : VisionLabel
    def __init__(self, master, lblText, height, yPos=None, relx=None, rely=None, relwidth=None, command=None, xDistance=180):
        VisionFrame.__init__(self, master)
        self.lblText = lblText
        self.yPos = yPos
        self.xDistance = xDistance
        self.command=command
        self.setupView()
        if yPos is not None:
            self.place(x=0, y=yPos, relwidth=1, height=height)
        elif relx is not None and rely is not None and relwidth is not None:
            self.place(relx=relx, rely=rely, relwidth=relwidth, height=height)


    def setupView(self):
        self.check_box_label = VisionLabel(self, text=self.lblText)
        self.check_box_label.place(x=5, y=0)

        self.chosenVar = BooleanVar()
        self.parameterCheckbox = VisionCheckBox(self, variable=self.chosenVar, command=self.clickCheckBox)
        self.parameterCheckbox.deselect()
        self.parameterCheckbox.place(x=self.xDistance, y=0, width= 25, height=25)

    def updateCheckboxLanguage(self, new_lang_label):
        self.check_box_label.config(text=new_lang_label)

    def clickCheckBox(self):
        if self.command is not None:
            self.command(self.getValue())

    def getValue(self):
        return self.chosenVar.get()

    def setValue(self, value):
        self.chosenVar.set(value)
