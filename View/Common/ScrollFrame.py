from View.Common.VisionUI import *

class ScrollView(VisionFrame):

    canvas: Canvas
    scrollVerticalBar: Scrollbar
    scrollHorizontalBar: Scrollbar
    view:  VisionFrame
    display:  VisionFrame = None
    canvas_window = None

    def __init__(self, master, displayHeight=None,displayWidth=None, scrollWidth=200, scrollHeight=1000, **kw):
        VisionFrame.__init__(self, master=master, **kw)
        self.scrollWidth = scrollWidth
        self.scrollHeight = scrollHeight
        self.displayHeight = displayHeight
        self.displayWidth = displayWidth
        self.setupScrollBar()
        self.bind("<Configure>", self.onResize)
        self.setupView()

    def setupScrollBar(self):
        if self.displayHeight is not None:
            self.scrollVerticalBar = Scrollbar(self, bg=Color.visionBg())
            self.scrollVerticalBar.pack(side=RIGHT, fill=Y)
        if self.displayWidth is not None:
            self.scrollHorizontalBar = Scrollbar(self, bg=Color.visionBg(), orient=HORIZONTAL)
            self.scrollHorizontalBar.pack(side=BOTTOM, fill=X)

    def setupView(self):
        self.canvas = Canvas(self)
        if self.displayHeight is not None:
            self.canvas.config(yscrollcommand=self.scrollVerticalBar.set)
            self.scrollVerticalBar.config(command=self.canvas.yview)

        if self.displayWidth is not None:
            self.canvas.config(xscrollcommand=self.scrollHorizontalBar.set)
            self.scrollHorizontalBar.config(command=self.canvas.xview)

        self.canvas.pack(side="left", fill="both", expand=True)

        self.view = VisionFrame(self.canvas)
        self.canvas_window = self.canvas.create_window((0,0), window=self.view, anchor="nw", tags="self.view")

        self.view.bind("<Configure>", self.onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)  # bind an event whenever the size of the viewPort frame changes.
        self.view.bind('<Enter>', self._bound_to_mousewheel)
        self.view.bind('<Leave>', self._unbound_to_mousewheel)
        self.onFrameConfigure(None)

        self.display = VisionFrame(self.view,
                                   width=self.winfo_width() if self.displayWidth is None else self.displayWidth,
                                   height=self.winfo_height() if self.displayHeight is None else self.displayHeight)
        self.display.grid(row=0, column=1)

    def setupDisplay(self, height, width=0):
        self.display = VisionFrame(self.view, width=self.winfo_width() if width == 0 else width, height=height)
        self.display.grid(row=0, column=1)

    def onResize(self, event):
        if self.display is not None:
            if self.displayWidth is None:
                self.display.config(width=int(0.95 * self.winfo_width()))
            if self.displayHeight is None:
                self.display.config(heigh=self.winfo_height())

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))  # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        if self.displayWidth is None:
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        if self.displayHeight is None:
            canvas_height = event.height
            self.canvas.itemconfig(self.canvas_window, width=canvas_height)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")