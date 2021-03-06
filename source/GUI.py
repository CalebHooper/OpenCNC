import tkinter as tk
from tkinter import filedialog
import threading
import Drawer

class GUI():

    def __init__(self, cnc):

        self.win = tk.Tk()
        self.win.minsize(800, 480)
        #self.win.attributes("-fullscreen", True)
        self.win.title("CNC User Interface")

        self.cnc = cnc

        # Construct GUI
        self.construct()

        # Tell The cnc of the GUI so it can interact with it as well.
        self.cnc.gui = self

        # GUI Loop Runs until program is done.
        self.win.mainloop()


    def construct(self):

        # ----- Init Image Assets -----

        self.pauseIcon  = tk.PhotoImage(file='./assets/Pause.png')
        self.cancelIcon = tk.PhotoImage(file='./assets/Cancel.png')
        self.playIcon   = tk.PhotoImage(file='./assets/Play.png')

        # --- Base Setup -----

        self.win.config(bg="#303030")

        parentFrame = tk.Frame(self.win, bg="#404040")
        parentFrame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        leftFrame = tk.Frame(parentFrame, bg="#606060")
        leftFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        rightFrame = tk.Frame(parentFrame, bg="#606060")
        rightFrame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        # ----- Control Panel Setup -----

        slide1 = tk.Frame(rightFrame, bg="#808080")
        slide1.pack(side=tk.LEFT, fill=tk.BOTH, padx= 5, pady=5, expand=True)
        slide2 = tk.Frame(rightFrame, bg="#808080")
        slide2.pack(side=tk.LEFT, fill=tk.BOTH, padx= 5, pady=5, expand=True)
        slide3 = tk.Frame(rightFrame, bg="#808080")
        slide3.pack(side=tk.LEFT, fill=tk.BOTH, padx= 5, pady=5, expand=True)
        slide4 = tk.Frame(rightFrame, bg="#808080")
        slide4.pack(side=tk.LEFT, fill=tk.BOTH, padx= 5, pady=5, expand=True)

        self.xDirSlider = tk.Scale(slide1, length = 207, from_=500, to=20, resolution=20, bg="#A09090", fg="black", highlightbackground="#C03030", troughcolor="#502020")
        self.xDirSlider.pack(side=tk.TOP, pady=5)
        self.xDirSlider.set(200)
        xSpeedTXT = tk.Text(slide1, bg="#A09090", highlightbackground="#C03030", relief=tk.FLAT)
        xSpeedTXT.insert(tk.INSERT, "x-Dir Speed")
        xSpeedTXT.configure(state="disabled", height=1, width=11)
        xSpeedTXT.pack(pady=5, padx=2)

        self.yDirSlider = tk.Scale(slide2, length = 207, from_=500, to=20, resolution=20, bg="#90A090", fg="black", highlightbackground="#30C030", troughcolor="#205020")
        self.yDirSlider.pack(side=tk.TOP, pady=5)
        self.yDirSlider.set(200)
        ySpeedTXT = tk.Text(slide2, bg="#90A090", highlightbackground="#30C030", relief=tk.FLAT)
        ySpeedTXT.insert(tk.INSERT, "y-Dir Speed")
        ySpeedTXT.configure(state="disabled", height=1, width=11)
        ySpeedTXT.pack(pady=5, padx=2)

        self.zDirSlider = tk.Scale(slide3, length = 207, from_=500, to=20, resolution=20, bg="#9090A0", fg="black", highlightbackground="#3030C0", troughcolor="#202050")
        self.zDirSlider.pack(side=tk.TOP, pady=5)
        self.zDirSlider.set(200)
        zSpeedTXT = tk.Text(slide3, bg="#9090A0", highlightbackground="#3030C0", relief=tk.FLAT)
        zSpeedTXT.insert(tk.INSERT, "z-Dir Speed")
        zSpeedTXT.configure(state="disabled", height=1, width=11)
        zSpeedTXT.pack(pady=5, padx=2)

        self.pwmDrill = tk.Scale(slide4, variable=tk.DoubleVar, length = 80, from_=1.0, to=0.0, resolution=.01, command=self.drillPulseChange, bg="#909090", fg="black", highlightbackground="#303030", troughcolor="#202020")
        self.pwmDrill.pack(side=tk.TOP, padx= 5, pady=5)
        self.pwmDrill.set(.5)
        pwmTXT = tk.Text(slide4, bg="#909090", highlightbackground="#303030", relief=tk.FLAT)
        pwmTXT.insert(tk.INSERT, "PWM Ratio")
        pwmTXT.configure(state="disabled", height=1, width=11)
        pwmTXT.pack(pady=5, padx=2)

        self.cycle = tk.Scale(slide4, variable=tk.DoubleVar, length = 80, from_=3.0, to=.1, resolution=.1, command=self.drillCycleChange, bg="#909090", fg="black", highlightbackground="#303030", troughcolor="#202020")
        self.cycle.pack(side=tk.TOP, padx=5, pady=5)
        self.cycle.set(.5)
        cycleTXT = tk.Text(slide4, bg="#909090", highlightbackground="#303030", relief=tk.FLAT)
        cycleTXT.insert(tk.INSERT, "Cycle Time")
        cycleTXT.configure(state="disabled", height=1, width=11)
        cycleTXT.pack(pady=5, padx=2)

        # ----- Log Panel SEtup -----

        logPanel = tk.Frame(self.win, bg="#404040")
        logPanel.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.log = tk.Text(logPanel, bg="black", height=64, width=512, fg="#00FF00")
        self.log.pack(padx=5, pady=5)

        self.LOGS = []

        # ----- CNC Control -----

        controlPanel = tk.Frame(leftFrame, bg="#808080")
        controlPanel.pack(fill=tk.BOTH, padx=5, pady=5)

        browseHolder = tk.Frame(controlPanel, bg="#606060")
        browseHolder.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        askFile = tk.Button(browseHolder, text="Browse", bg="white", command=self.getFile)
        askFile.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

        self.selectedFile = tk.Text(browseHolder, bg="white")
        self.selectedFile.insert(tk.INSERT, "No file selcted.")
        self.selectedFile.configure(state="disabled", height=1, width=20)
        self.selectedFile.pack(side=tk.LEFT, expand=True)

        drawButton = tk.Button(browseHolder, text="Draw", bg="white", command=self.drawDXF)
        drawButton.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

        controlButtonHolder = tk.Frame(controlPanel, bg="#606060")
        controlButtonHolder.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(0, 5))

        startPrint = tk.Button(controlButtonHolder, height=64, width=64, bg="#606060", highlightbackground="#606060", relief=tk.FLAT, activebackground="#606060")
        startPrint.config(image=self.playIcon, pady=3)
        startPrint.pack(side=tk.LEFT, expand=True)

        pausePrint = tk.Button(controlButtonHolder, height=64, width=64, bg="#606060", highlightbackground="#606060", relief=tk.FLAT,activebackground="#606060")
        pausePrint.config(image=self.pauseIcon, pady=3)
        pausePrint.pack(side=tk.LEFT, expand=True)

        cancelPrint = tk.Button(controlButtonHolder, height=64, width=64, bg="#606060", highlightbackground="#606060", relief=tk.FLAT, activebackground="#606060")
        cancelPrint.config(image=self.cancelIcon, pady=3)
        cancelPrint.pack(side=tk.LEFT, expand=True)

        # ----- CNC Move -----

        moverPanel = tk.Frame(leftFrame, bg="#808080")
        moverPanel.pack(fill=tk.BOTH, padx=5, pady=5)     

        xyDirHolder= tk.Frame(moverPanel, width=100, height=100, bg="#606060")
        xyDirHolder.pack(side=tk.LEFT, expand=True, padx=(5, 0), pady=5)

        topLevel = tk.Frame(xyDirHolder, bg="#606060")
        topLevel.pack(padx=5, pady=5)
        midLevel = tk.Frame(xyDirHolder, bg="#606060")
        midLevel.pack(padx=5, pady=5)
        bottomLevel = tk.Frame(xyDirHolder, bg="#606060")
        bottomLevel.pack(padx=5, pady=5)

        up = tk.Button(topLevel, width=3, text="Y+", bg="#90A090", highlightbackground="#30C030", activebackground="#205020")
        up.pack(side=tk.TOP)
        up.bind("<Button-1>", self.startYMotorClock)
        up.bind("<ButtonRelease-1>", self.stopYMotor)

        right = tk.Button(midLevel, width=3, text="X+", bg="#A09090", highlightbackground="#C03030", activebackground="#502020")
        right.pack(side=tk.RIGHT, padx=10)
        right.bind("<Button-1>", self.startXMotorClock)
        right.bind("<ButtonRelease-1>", self.stopXMotor)

        down = tk.Button(bottomLevel, width=3, text="Y-", bg="#90A090", highlightbackground="#30C030", activebackground="#205020")
        down.pack(side=tk.BOTTOM)
        down.bind("<Button-1>", self.startYMotorCounterClock)
        down.bind("<ButtonRelease-1>", self.stopYMotor)

        left = tk.Button(midLevel, width=3, text="X-", bg="#A09090", highlightbackground="#C03030", activebackground="#502020")
        left.pack(side=tk.LEFT, padx=10)
        left.bind("<Button-1>", self.startXMotorCounterClock)
        left.bind("<ButtonRelease-1>", self.stopXMotor)

        zDirHolder= tk.Frame(moverPanel, width=50, height=100, bg="#606060")
        zDirHolder.pack(side=tk.LEFT, expand=True, padx=(5, 0), pady=5, fill=tk.Y)

        zPlus = tk.Button(zDirHolder,width=3, text="Z+", bg="#9090A0", highlightbackground="#3030C0", activebackground="#202050")
        zPlus.pack(side=tk.TOP, padx=5, pady=5)
        zPlus.bind("<Button-1>", self.startZMotorClock)
        zPlus.bind("<ButtonRelease-1>", self.stopZMotor)

        zMinus = tk.Button(zDirHolder, width=3, text="Z-", bg="#9090A0", highlightbackground="#3030C0", activebackground="#202050")
        zMinus.pack(side=tk.BOTTOM, padx=5, pady=5)
        zMinus.bind("<Button-1>", self.startZMotorCounterClock)
        zMinus.bind("<ButtonRelease-1>", self.stopZMotor)

        drillHolder= tk.Frame(moverPanel, width=50, height=100, bg="#606060")
        drillHolder.pack(side=tk.LEFT, expand=True, padx=5, pady=5, fill=tk.Y)

        drillOn = tk.Button(drillHolder,width=4, text="Drill On", bg="#909090", highlightbackground="#303030", activebackground="#202020", command=self.startDrill)
        drillOn.pack(side=tk.TOP, padx=5, pady=5)

        drillOff = tk.Button(drillHolder, width=4, text="Drill Off", bg="#909090", highlightbackground="#303030", activebackground="#202020", command=self.cnc.stopDrilling)
        drillOff.pack(side=tk.BOTTOM, padx=5, pady=5)

    def addLogMessage(self, message):

        self.LOGS.append(message)
        self.log.delete(1.0, tk.END)

        if(len(self.LOGS) < 64):
            for i in range(64 - len(self.LOGS)):
                self.log.insert(tk.END, '\n')

        for mes in self.LOGS:
            self.log.insert(tk.END, "\n" + mes)

        self.log.see(tk.END)
        
    def getFile(self):
        self.printFile = filedialog.askopenfilename(initialdir = "/media", title = "Select DXF Print file",filetypes = (("dxf Files","*.DXF"),("all files","*.*")))

        self.selectedFile.config(state="normal")
        self.selectedFile.delete(1.0, tk.END)
        self.selectedFile.insert(tk.INSERT, str(self.printFile)[-24:])
        self.selectedFile.config(state="disabled")

        self.addLogMessage("Selected file: " + self.printFile)

    def drawDXF(self):

        if hasattr(self, 'printFile'):
            drawer = Drawer.Drawer(self.printFile, self.cnc)
        else:
            self.addLogMessage("ERROR: No file selected.")

    def drillCycleChange(self, val):
        self.cnc.updateDrillSettings(val, val)

    def drillPulseChange(self, val):
        self.cnc.updateDrillSettings(val, val)

    def startDrill(self):
        self.cnc.startDrill(self.pwmDrill.get(), self.cycle.get())


    def startXMotorClock(self, e):
        self.cnc.startMotor("X", self.xDirSlider.get(), 1)
        self.addLogMessage("Update: Starting X+ Motor Clockwise")

    def stopXMotor(self, e):
        self.cnc.stopMotor("X")
        self.addLogMessage("Update: Stopping X Motor")

    def startXMotorCounterClock(self, e):
        self.cnc.startMotor("X", self.xDirSlider.get(), 0)
        self.addLogMessage("Update: Starting X- Motor Counter Clockwise")


    def startYMotorClock(self, e):
        self.cnc.startMotor("Y", self.yDirSlider.get(), 1)
        self.addLogMessage("Update: Starting Y+ Motor Clockwise")

    def stopYMotor(self, e):
        self.cnc.stopMotor("Y")
        self.addLogMessage("Update: Stopping Y Motor")

    def startYMotorCounterClock(self, e):
        self.cnc.startMotor("Y", self.yDirSlider.get(), 0)
        self.addLogMessage("Update: Starting Y- Motor Counter Clockwise")


    def startZMotorClock(self, e):
        self.cnc.startMotor("Z", self.zDirSlider.get(), 1)
        self.addLogMessage("Update: Starting Z+ Motor Clockwise")

    def stopZMotor(self, e):
        self.cnc.stopMotor("Z")
        self.addLogMessage("Update: Stopping Z Motor")

    def startZMotorCounterClock(self, e):
        self.cnc.startMotor("Z", self.zDirSlider.get(), 0)
        self.addLogMessage("Update: Starting Z- Motor Counter Clockwise")

