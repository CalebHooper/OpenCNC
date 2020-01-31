import threading
import time
import ctypes
import GUI

IS_RPI = True

try:
    import RPi.GPIO as GPIO

except:
    IS_RPI = False
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

class MotorThread(threading.Thread):

    def __init__(self, STEP_PIN, DIR_PIN, SPEED):

        threading.Thread.__init__(self)

        self.STEP_PIN = STEP_PIN
        self.DIR_PIN = DIR_PIN

        self.DIR = 0

        self.RUNNING = True
        self.SPINNING = False

        self.SPEED = SPEED
        self.DELAY = (1/ self.SPEED) / 2



    def run(self):

        global IS_RPI

        while self.RUNNING:
            
            if not self.SPINNING:
                continue

            if not IS_RPI:
                continue

            GPIO.output(self.DIR_PIN, self.DIR)

            GPIO.output(self.STEP_PIN, 0)
            time.sleep(self.DELAY)

            GPIO.output(self.STEP_PIN, 1)
            time.sleep(self.DELAY)


    def startMotor(self, SPEED):

        self.SPEED = SPEED
        self.DELAY = (1/ self.SPEED) / 2
        self.SPINNING = True


    def stopMotor(self):

        self.SPINNING = False

    def setMotorSpeed(self, SPEED):

        self.SPEED = SPEED
        self.DELAY = (1/ self.SPEED) / 2

    def setDir(self, DIR):
        self.DIR = DIR












class CNC():

    def __init__(self, X_MOTORS, X_DIR, Y_MOTORS, Y_DIR, Z_MOTORS, Z_DIR, DRILL_PIN, TABLE_WIDTH, TABLE_HEIGHT, TABLE_UNITS):

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

        self.MOTORX_PIN = X_MOTORS
        self.X_DIR_PIN    = X_DIR

        self.MOTORY_PIN = Y_MOTORS
        self.Y_DIR_PIN    = Y_DIR

        self.MOTORZ_PIN = Z_MOTORS
        self.Z_DIR_PIN    = Z_DIR

        self.DRILL_PIN = DRILL_PIN

        # Setup Raspberry Pi pins
        try:
            GPIO.setup(self.MOTORX_PIN, GPIO.OUT)
            GPIO.setup(self.X_DIR_PIN, GPIO.OUT)

            GPIO.setup(self.MOTORY_PIN, GPIO.OUT)
            GPIO.setup(self.Y_DIR_PIN, GPIO.OUT)

            GPIO.setup(self.MOTORZ_PIN, GPIO.OUT)
            GPIO.setup(self.Z_DIR_PIN, GPIO.OUT)

            GPIO.setup(self.DRILL_PIN, GPIO.OUT)
        except:
            print("ERROR: Can not set input output pins device may not be a Raspberry Pi")

        # Create Motor threads
        self.X_THREAD = MotorThread(self.MOTORX_PIN, self.X_DIR_PIN, 200)
        self.X_THREAD.start()

        self.Y_THREAD = MotorThread(self.MOTORY_PIN, self.Y_DIR_PIN, 200)
        self.Y_THREAD.start()

        self.Z_THREAD = MotorThread(self.MOTORZ_PIN, self.Z_DIR_PIN, 200)
        self.Z_THREAD.start()

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

        # KILL THE MOTOR THREAD
        self.X_THREAD.RUNNING = False
        self.Y_THREAD.RUNNING = False
        self.Z_THREAD.RUNNING = False

    def logMessage(self, mes):

        print(mes)

        if hasattr(self, 'gui'):
            self.gui.addLogMessage(mes)





        
        
