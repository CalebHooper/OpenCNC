import tkinter as tk
import threading

class GUI():

    def __init__(self, cnc):

        self.win = tk.Tk()
        self.win.minsize(600, 500)
        #self.win.attributes("-fullscreen", True)
        self.win.title("CNC User Interface")

        self.cnc = cnc

        self.run()



    def run(self):

        # --- Base Setup -----

        parentFrame = tk.Frame(self.win, bg="#000000")
        parentFrame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        leftFrame = tk.Frame(parentFrame, bg="#202020")
        leftFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2, pady=2)

        rightFrame = tk.Frame(parentFrame, bg="#202020")
        rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=2, pady=2)

        tk.Button(leftFrame, text="QUIT", width=100, height=100, command=self.win.quit).pack(side=tk.LEFT)

        # ----- Control Panel Setup -----

        controlPanel = tk.Frame(rightFrame, bg="#404040")
        controlPanel.pack( fill=tk.BOTH, padx=5, pady=5)

        slideHolder = tk.Frame(controlPanel, bg = "#5050FF")
        slideHolder.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        slide1 = tk.Frame(slideHolder, bg="#FF0000")
        slide1.pack(side=tk.LEFT, fill=tk.BOTH, padx= 5, pady=5)
        slide2 = tk.Frame(slideHolder, bg="#00FF00")
        slide2.pack(side=tk.LEFT, fill=tk.BOTH, padx= 5, pady=5)
        slide3 = tk.Frame(slideHolder, bg="#0000FF")
        slide3.pack(side=tk.LEFT, fill=tk.BOTH, padx= 5, pady=5)
        slide4 = tk.Frame(slideHolder, bg="#FFFF00")
        slide4.pack(side=tk.LEFT, fill=tk.BOTH, padx= 5, pady=5)

        xDirSlider = tk.Scale(slide1, label="X-Dir Speed", length = 140, from_=500, to=20, resolution=20, command=self.xSlideChange)
        xDirSlider.pack(side=tk.TOP)
        xDirSlider.set(200)

        yDirSlider = tk.Scale(slide2, label="Y-Dir Speed", length = 140, from_=500, to=20, resolution=20, command=self.ySlideChange)
        yDirSlider.pack(side=tk.TOP)
        yDirSlider.set(200)

        zDirSlider = tk.Scale(slide3, label="Z-Dir Speed", length = 140, from_=500, to=20, resolution=20, command=self.zSlideChange)
        zDirSlider.pack(side=tk.TOP)
        zDirSlider.set(200)

        pwmDrill = tk.Scale(slide4, orient=tk.HORIZONTAL, label="PWM Ratio", from_=0.0, to=1.0, variable=tk.DoubleVar, resolution=.01, command=self.drillPulseChange)
        pwmDrill.pack(side=tk.TOP, padx= 5, pady=5)
        pwmDrill.set(.5)
        cycle = tk.Scale(slide4, orient=tk.HORIZONTAL, label="Cycle Time", from_=0.1, to=10.0, variable=tk.DoubleVar, resolution=.05, command=self.drillCycleChange)
        cycle.pack(side=tk.TOP, padx=5, pady=5)
        cycle.set(.5)

        # ----- Log Panel SEtup -----

        logPanel = tk.Frame(rightFrame, bg="#404040")
        logPanel.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        #controlFrame = tk.Frame(self.win, width= 300, height =200, bg="gray")
        #controlFrame.pack(side = tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        #tk.Label(controlFrame, text="asdasd").pack()

        #tk.Label(self.win, text="TEST LABEL").pack()
        #tk.Button(self.win, text="IM A BUTTON").pack()
        #tk.Scale(self.win).pack()

        self.win.mainloop()


    def xSlideChange(self, val):
        print("HELLO" + val)

    def ySlideChange(self, val):
        print("HELLO" + val)

    def zSlideChange(self, val):
        print("HELLO" + val)

    def drillCycleChange(self, val):
        self.cnc.updateDrillPWM(val)

    def drillPulseChange(self, val):
        self.cnc.updateDrillCycle(val)
