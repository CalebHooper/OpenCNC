import threading
import time
import ctypes
import GUI

# Wether or not the dvice is a raspberry Pi
IS_RPI = True

try:
    import RPi.GPIO as GPIO

except:
    IS_RPI = False
    print("ERROR: This device most likely is not a raspberry PI the program will still run although controls will have no affect. If this is a Raspberry Pi god save you.")

class CNC():

    def __init__(self, motorsX, dirX, motorsY, dirY, motorsZ, dirZ, drill, cncWidth, cncHeight, cncUnits):

        # Save data needed to operate CNC
        self.cncHeight      = cncHeight
        self.cncWidth       = cncWidth
        self.cncUnits       = cncUnits

        self.stepX          = motorsX
        self.dirX           = dirX

        self.stepY          = motorsY
        self.dirY           = dirY

        self.stepZ          = motorsZ
        self.dirZ           = dirZ

        self.drill          = drill

        # Setup Raspberry Pi pins
        if IS_RPI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)

            GPIO.setup(self.stepX, GPIO.OUT)
            GPIO.setup(self.dirX, GPIO.OUT)

            GPIO.setup(self.stepY, GPIO.OUT)
            GPIO.setup(self.dirY, GPIO.OUT)

            GPIO.setup(self.stepZ, GPIO.OUT)
            GPIO.setup(self.dirZ, GPIO.OUT)

            GPIO.setup(self.drill, GPIO.OUT)

    def startDrill(self, drillPwm, drillCycle):

        # Stop any action the drill may already be doing
        if hasattr(self, 'drillThread'):
            self.drillThread.stopDrillInternal()
            self.drillThread = DrillThread(self.drill, drillPwm, drillCycle)
            self.drillThread.start()
        else:
            self.drillThread = DrillThread(self.drill, drillPwm, drillCycle)
            self.drillThread.start()

        self.logMessage("UPDATE: Drill has started.")

    def stopDrilling(self):

        if hasattr(self, 'drillThread'):
            self.drillThread.stopDrillInternal()
            del self.drillThread
            self.logMessage("UPDATE: Drill is stopping...")
        else:
            self.logMessage("WARNING: Can't stop drill no drill currently running.")

    def updateDrillSettings(self, drillPwm, drillCycle):

        if hasattr(self, 'drillThread'):
            self.drillThread.updateDrillSettingsInternal(drillPwm, drillCycle)
        else:
            self.logMessage("WARNING: Can't update drill PWM no drill running.")

    def startMotor(self, motor, speed, dir):

        if motor == "X":

            if hasattr(self, "motorThreadX"):
                self.motorThreadX.stopMotorInternal()
                self.motorThreadX = MotorThread(self.stepX, self.dirX, speed, dir)
            else:
                self.motorThreadX = MotorThread(self.stepX, self.dirX, speed, dir)

        elif motor == "Y":

            if hasattr(self, "motorThreadY"):
                self.motorThreadY.stopMotorInternal()
                self.motorThreadY = MotorThread(self.stepY, self.dirY, speed, dir)
            else:
                self.motorThreadY = MotorThread(self.stepY, self.dirY, speed, dir)

        elif motor == "Z":

            if hasattr(self, "motorThreadZ"):
                self.motorThreadZ.stopMotorInternal()
                self.motorThreadZ = MotorThread(self.stepZ, self.dirZ, speed, dir)
            else:
                self.motorThreadZ = MotorThread(self.stepZ, self.dirZ, speed, dir)

        self.logMessage("Update: Motor " + motor + " has been started.")

    def stopMotor(self, motor):

        if motor == "X":

            if hasattr(self, "motorThreadX"):
                self.motorThreadX.stopMotorInternal()

        elif motor == "Y":

            if hasattr(self, "motorThreadY"):
                self.motorThreadY.stopMotorInternal()

        elif motor == "Z":

            if hasattr(self, "motorThreadZ"):
                self.motorThreadZ.stopMotorInternal()

        self.logMessage("Update: Motor " + motor + " has been stoped.")

    def updateMotorSettings(self, motor, speed, dir):

        if motor == "X":

            if hasattr(self, "motorThreadX"):
                self.motorThreadX.setMotorSettingsInternal(speed, dir)

        elif motor == "Y":

            if hasattr(self, "motorThreadY"):
                self.motorThreadY.setMotorSettingsInternal(speed, dir)

        elif motor == "Z":

            if hasattr(self, "motorThreadZ"):
                self.motorThreadZ.setMotorSettingsInternal(speed, dir)

        self.logMessage("Update: Motor " + motor + " has been updated.")

    def logMessage(self, mes):

        print(mes)

        if hasattr(self, 'gui'):
            self.gui.addLogMessage(mes)

    def clean(self):

        # Kill The Drill Thread If Currently Running
        if hasattr(self, 'drillThread'):
            self.drillThread.stopDrillInternal()
            del self.drillThread

        # Kill The Drill Thread If Currently Running
        if hasattr(self, 'motorThreadX'):
            self.motorThreadX.stopMotor()
            del self.motorThreadX

        # Kill The Drill Thread If Currently Running
        if hasattr(self, 'motorThreadY'):
            self.motorThreadY.stopMotor()
            del self.motorThreadY

        # Kill The Drill Thread If Currently Running
        if hasattr(self, 'motorThreadZ'):
            self.motorThreadZ.stopMotor()
            del self.motorThreadZ


class DrillThread (threading.Thread):

    def __init__ (self, drillPin, drilPwm, drillCycle):

        threading.Thread.__init__(self)

        self.drillPin   = drillPin 
        self.drillPwm    = drilPwm
        self.drillCycle = drillCycle

        self.drillRunning = True

    def run(self):

        while self.drillRunning:

            if not IS_RPI:
                continue

            # Turn drill on
            GPIO.output(self.DRILL_PIN, 1)
            time.sleep(float(self.CYCLE_LENGTH) * (float(self.PWM)))

            # Turn drill off
            GPIO.output(self.DRILL_PIN, 0)
            time.sleep(float(self.CYCLE_LENGTH) * (1.0 - float(self.PWM)))

    def updateDrillSettingsInternal(self, drillPwm, drillCycle):

        self.drillPwm = drillPwm
        self.drillCycle = drillCycle

    def stopDrillInternal(self):

        self.drillRunning = False

class MotorThread(threading.Thread):

    def __init__(self, stepPin, dirPin, speed, dir):

        threading.Thread.__init__(self)

        self.stepPin    = stepPin
        self.dirPin     = dirPin

        self.running    = True

        self.setMotorSettingsInternal(speed, dir)

    def run(self):

        while self.running:

            if not IS_RPI:
                continue

            GPIO.output(self.stepPin, 0)
            time.sleep(self.delay)

            GPIO.output(self.stepPin, 1)
            time.sleep(self.delay)

    def setMotorSettingsInternal(self, speed, dir):

        self.delay = (1 / speed) / 2
        self.dir = dir


    def stopMotorInternal(self):

        self.running = False








        
        
