from tkinter.font import Font


def boldFont(size=12):
    return Font(family="Helvetica", weight="bold", size=size)

def regularFont(size=12):
    return Font(family="Helvetica", weight="normal", size=size)

def stepSettingFont():
    return boldFont(10)