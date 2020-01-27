import threading
import time
import ctypes

try:
    import RPi.GPIO as GPIO

except:
    print("ERROR: NOT A RASPBERRY PI")

class DrillThread (threading.Thread):

    def __init__ (self, DRILL_PIN, DRILL_PWM, CYCLE_LENGTH):

        threading.Thread.__init__(self)

        self.DRILL_PIN = DRILL_PIN 
        self.PWM = DRILL_PWM
        self.CYCLE_LENGTH = CYCLE_LENGTH

        self.DRILL_STATUS = True

    def run(self):


        while self.DRILL_STATUS:

            # Turn drill on
            try:
                GPIO.output(self.DRILL_PIN, 1)
            except:
                print("ERROR: NOT A RASPBERRY PI")

            time.sleep(self.CYCLE_LENGTH * self.PWM)

            # Turn drill off
            try:
                GPIO.output(self.DRILL_PIN, 0)
            except:
                print("ERROR: NOT A RASPBERRY PI")

            print("DRILLING!!")
            time.sleep(self.CYCLE_LENGTH * (1 - self.PWM))

        print("DRILL HAS STOPPED")



class CNC():

    def __init__(self, X_MOTOR_1, X_MOTOR_2, Y_MOTOR_1, Y_MOTOR_2, Z_MOTOR_1, Z_MOTOR_2, DRILL_PIN):

        # Init pi output
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
        except:
            print("ERROR: NOT A RASPBERRY PI")

        # Save values
        self.MOTOR_X1 = X_MOTOR_1
        self.MOTOR_X2 = X_MOTOR_2

        self.MOTOR_Y1 = Y_MOTOR_1
        self.MOTOR_Y2 = Y_MOTOR_2

        self.MOTOR_Z1 = Z_MOTOR_1
        self.MOTOR_Z2 = Z_MOTOR_2

        self.DRILL_PIN = DRILL_PIN

        try:
            GPIO.setup(self.MOTOR_X1, GPIO.OUT)
            GPIO.setup(self.MOTOR_X2, GPIO.OUT)

            GPIO.setup(self.MOTOR_Y1, GPIO.OUT)
            GPIO.setup(self.MOTOR_Y2, GPIO.OUT)

            GPIO.setup(self.MOTOR_Z1, GPIO.OUT)
            GPIO.setup(self.MOTOR_Z2, GPIO.OUT)

            GPIO.setup(self.DRILL_PIN, GPIO.OUT)
        except:
            print("ERROR: NOT A RASPBERRY PI")

    def startDrill(self, PWM_RATIO, CYCLE_LENGTH):

        # Stop any action the drill may already be doing
        try:
            self.drillThread
        except:
            self.drillThread = DrillThread(self.DRILL_PIN, PWM_RATIO, CYCLE_LENGTH)
            self.drillThread.start()
        else:
            self.drillThread.DRILL_STATUS = False
            self.drillThread = DrillThread(self.DRILL_PIN, PWM_RATIO, CYCLE_LENGTH)
            self.drillThread.start()

    def updateDrillPWM(self, pwm):
        try:
            self.drillThread
        except:
            print("No Drill Running")
        else:
            self.drillThread.PWM = pwm


    def updateDrillCycle(self, cycle):
        try:
            self.drillThread
        except:
            print("No Drill Running")
        else:
            self.drillThread.PWM = cycle


    def stopDrilling(self):
        try:
            self.drillThread
        except:
            print("NO DRILL RUNNING")
        else:
            self.drillThread.DRILL_STATUS = False
            del self.drillThread


        
        
