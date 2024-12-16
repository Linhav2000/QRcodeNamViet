import random
from View.Common.VisionUI import *
import threading

list_name = [
    ["A Linh", "Đức Vision"],
    ["A Khôi", "Công"],
    ["A Kiên", "Kato"],
    ["Đức Cứng", "A Huy"],
    # ["A Thịnh",""]
]
def reset_label():
    label_team1_no1.config(text="No 1")
    label_team1_no2.config(text="No 2")
    label_team1_no3.config(text="No 3")
    label_team1_no4.config(text="No 4")
    label_team1_no5.config(text="No 5")
    label_team1_no6.config(text="No 6")

    label_team2_no1.config(text="No 1")
    label_team2_no2.config(text="No 2")
    label_team2_no3.config(text="No 3")
    label_team2_no4.config(text="No 4")
    label_team2_no5.config(text="No 5")
    label_team2_no6.config(text="No 6")

def randomCalculate():
    reset_label()
    # team1 = []
    # team2 = []
    # random_display(names=list1, display1=label_team1_no1, display2=label_team2_no1)
    # random_display(names=list2, display1=label_team1_no2, display2=label_team2_no2)
    # random_display(names=list3, display1=label_team1_no3, display2=label_team2_no3)
    # random_display(names=list4, display1=label_team1_no4, display2=label_team2_no4)
    # # random_display(names=list5, display1=label_team1_no5, display2=label_team2_no5)
    # random_display(names=list6, display1=label_team1_no6, display2=label_team2_no6)
    #
    for idx, pair in enumerate(list_name):
        random_display(names=pair, display1=list_label_team1[idx], display2=list_label_team2[idx])


mainView = VisionTopLevel()


width = 623
height = 523
mainView.title("Choose Football team")
mainView.iconbitmap('./resource/appIcon.ico')
mainView.geometry("{}x{}".format(width, height))
mainView.resizable(0, 0)
mainView.grab_set()

btnRandom = VisionButton(mainView, text="Random", fg=Color.winDarkOrange(), font=VisionFont.boldFont(20), command=randomCalculate)
btnRandom.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)

height=0.12
team1_frame = VisionFrame(mainView, bg=Color.winDarkOrange())
team2_frame = VisionFrame(mainView, bg=Color.winDarkOrange())

team1_frame.place(relx=0.01, rely=0.01, relwidth=0.48, relheight=0.7)
team2_frame.place(relx=0.51, rely=0.01, relwidth=0.48, relheight=0.7)

label_team1 = VisionLabel(team1_frame, text="Team 1(Áo Xanh):", bg=Color.winDarkOrange(), font=VisionFont.boldFont(20))
label_team1.place(relx=0, rely=0.01, relwidth=1, relheight=0.15)

label_team1_no1 = VisionLabel(team1_frame, text="No 1", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team1_no1.place(relx=0, rely=0.2, relwidth=1, relheight=0.15)

label_team1_no2 = VisionLabel(team1_frame, text="No 2", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team1_no2.place(relx=0, rely=0.2 + height, relwidth=1, relheight=0.15)

label_team1_no3 = VisionLabel(team1_frame, text="No 3", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team1_no3.place(relx=0, rely=0.2 + 2*height, relwidth=1, relheight=0.15)

label_team1_no4 = VisionLabel(team1_frame, text="No 4", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team1_no4.place(relx=0, rely=0.2 + 3*height, relwidth=1, relheight=0.15)

label_team1_no5 = VisionLabel(team1_frame, text="No 5", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team1_no5.place(relx=0, rely=0.2 + 4*height, relwidth=1, relheight=0.15)

label_team1_no6 = VisionLabel(team1_frame, text="No 6", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team1_no6.place(relx=0, rely=0.2 + 5*height, relwidth=1, relheight=0.15)

label_team2 = VisionLabel(team2_frame, text="Team 2(Áo Đỏ): ", bg=Color.winDarkOrange(), font=VisionFont.boldFont(20))
label_team2.place(relx=0, rely=0.01, relwidth=1, relheight=0.15)

label_team2_no1 = VisionLabel(team2_frame, text="No 1", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team2_no1.place(relx=0, rely=0.2, relwidth=1, relheight=0.15)

label_team2_no2 = VisionLabel(team2_frame, text="No 2", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team2_no2.place(relx=0, rely=0.2 + height, relwidth=1, relheight=0.15)

label_team2_no3 = VisionLabel(team2_frame, text="No 3", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team2_no3.place(relx=0, rely=0.2 + 2*height, relwidth=1, relheight=0.15)

label_team2_no4 = VisionLabel(team2_frame, text="No 4", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team2_no4.place(relx=0, rely=0.2 + 3*height, relwidth=1, relheight=0.15)

label_team2_no5 = VisionLabel(team2_frame, text="No 5", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team2_no5.place(relx=0, rely=0.2 + 4*height, relwidth=1, relheight=0.15)

label_team2_no6 = VisionLabel(team2_frame, text="No 6", bg=Color.winDarkOrange(), font=VisionFont.boldFont(16))
label_team2_no6.place(relx=0, rely=0.2 + 5*height, relwidth=1, relheight=0.15)

list_label_team1 = [label_team1_no1, label_team1_no2, label_team1_no3, label_team1_no4, label_team1_no5, label_team1_no6]
list_label_team2 = [label_team2_no1, label_team2_no2, label_team2_no3, label_team2_no4, label_team2_no5, label_team2_no6]


def display_label(display:VisionLabel, text):
    display_threading = threading.Thread(target=display_thread, args=(display, text))
    display_threading.start()

def display_thread(display:VisionLabel, text):
    display.set(text)

def random_display(names, display1: VisionLabel, display2: VisionLabel):
    if len(names) < 1:
        return
    _names = names.copy()
    global list_name
    for _ in range(20):
        for name in list_name:
            TimeControl.sleep(5)
            display_label(display1, name)
            display_label(display2, name)
            mainView.update()
            # mainView.after(100, )
    choice1 = random.choice(_names)
    _names.remove(choice1)
    choice2 = _names[0]
    display_label(display1, choice1)
    display_label(display2, choice2)

mainView.mainloop()