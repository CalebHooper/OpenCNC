import threading
import time
import ctypes
import GUI

try:
    import RPi.GPIO as GPIO

except:
    print("ERROR: Can't RPi wither not avaible or device is not a raspberry pi.")

class DrillThread (threading.Thread):

    def __init__ (self, DRILL_PIN, DRILL_PWM, CYCLE_LENGTH):

        threading.Thread.__init__(self)

        self.DRILL_PIN = DRILL_PIN 
        self.PWM = DRILL_PWM
        self.CYCLE_LENGTH = CYCLE_LENGTH

        self.DRILL_STATUS = True

    def mySleep(self, dur):

        if dur > 0 and dur <= 10:
            time.sleep(dur)


    def run(self):


        while self.DRILL_STATUS:

            # Turn drill on
            try:
                GPIO.output(self.DRILL_PIN, 1)
            except:
                print("ERROR: NOT A RASPBERRY PI")

            self.mySleep(float(self.CYCLE_LENGTH) * (float(self.PWM)))


            # Turn drill off
            try:
                GPIO.output(self.DRILL_PIN, 0)
            except:
                print("ERROR: NOT A RASPBERRY PI")

            self.mySleep(float(self.CYCLE_LENGTH) * (1.0 - float(self.PWM)))

class CNC():

    def __init__(self, X_MOTOR_1, X_MOTOR_2, X_DIR, Y_MOTOR_1, Y_MOTOR_2, Y_DIR, Z_MOTOR_1, Z_MOTOR_2, Z_DIR, DRILL_PIN, TABLE_WIDTH, TABLE_HEIGHT, TABLE_UNITS):

        # Init pi output
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
        except:
            print("ERROR: Can not set mode device may not me a raspberry Pi")

        # Save values
        self.TABLE_HEIGHT = TABLE_HEIGHT
        self.TABLE_WIDTH = TABLE_WIDTH
        self.TABLE_UNITS = TABLE_UNITS

        self.MOTOR_X1_PIN = X_MOTOR_1
        self.MOTOR_X2_PIN = X_MOTOR_2
        self.X_DIR_PIN    = X_DIR

        self.MOTOR_Y1_PIN = Y_MOTOR_1
        self.MOTOR_Y2_PIN = Y_MOTOR_2
        self.Y_DIR_PIN    = Y_DIR

        self.MOTOR_Z1_PIN = Z_MOTOR_1
        self.MOTOR_Z2_PIN = Z_MOTOR_2
        self.Z_DIR_PIN    = Z_DIR

        self.DRILL_PIN = DRILL_PIN

        # Setup Raspberry Pi pins
        try:
            #GPIO.setup(self.MOTOR_X1, GPIO.OUT)
            #GPIO.setup(self.MOTOR_X2, GPIO.OUT)

            #GPIO.setup(self.MOTOR_Y1, GPIO.OUT)
            #GPIO.setup(self.MOTOR_Y2, GPIO.OUT)

            #GPIO.setup(self.MOTOR_Z1, GPIO.OUT)
            #GPIO.setup(self.MOTOR_Z2, GPIO.OUT)

            GPIO.setup(self.DRILL_PIN, GPIO.OUT)
        except:
            print("ERROR: Can not set input output pins device may not be a Raspberry Pi")

    def startDrill(self, PWM_RATIO, CYCLE_LENGTH):

        # Stop any action the drill may already be doing
        if hasattr(self, 'drillThread'):
            self.drillThread.DRILL_STATUS = False
            self.drillThread = DrillThread(self.DRILL_PIN, PWM_RATIO, CYCLE_LENGTH)
            self.drillThread.start()
        else:
            self.drillThread = DrillThread(self.DRILL_PIN, PWM_RATIO, CYCLE_LENGTH)
            self.drillThread.start()

        self.logMessage("UPDATE: Drill has started.")

    def updateDrillPWM(self, pwm):

        if hasattr(self, 'drillThread'):
            self.drillThread.PWM = pwm
        else:
            self.logMessage("WARNING: Can't update drill PWM no drill running.")

    def updateDrillCycle(self, cycle):

        if hasattr(self, 'drillThread'):
            self.drillThread.CYCLE_LENGTH = cycle
        else:
            self.logMessage("WARNING: Can't update drill cycle no drill running.")

    def stopDrilling(self):

        if hasattr(self, 'drillThread'):
            self.drillThread.DRILL_STATUS = False
            del self.drillThread
            self.logMessage("UPDATE: Drill is stopping...")
        else:
            self.logMessage("WARNING: Can't stop drill no drill currently running.")

    def clean(self):

        # Kill The Drill Thread If Currently Running
        if hasattr(self, 'drillThread'):
            self.drillThread.DRILL_STATUS = False
            del self.drillThread

    def logMessage(self, mes):

        print(mes)

        if hasattr(self, 'gui'):
            self.gui.addLogMessage(mes)





        
        
