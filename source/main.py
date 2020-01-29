import sys
import DXF
import CNC
import time
import GUI

# Global Variables
VERIFY_WINDOW_SIZE = 1000

# Infomation about your cnc
CNC_WIDTH = 20
CNC_HEIGHT = 20
CNC_UNITS = DXF.INCHES

# GPIO Pi output pin configuration
# These pins are used to control the CNC
X_MOTOR_1   = 16
X_MOTOR_2   = 20
X_DIR       = 21

Y_MOTOR_1   = 25
Y_MOTOR_2   = 8
Y_DIR       = 7

Z_MOTOR_1   = 17
Z_MOTOR_2   = 27
Z_DIR       = 22

DRILL_PIN   = 4

# GPIO pi input pins configuration
# These  pins are used to stop the CNC in case it goes to far.
X_SAFE_1 = 5
X_SAFE_2 = 6

Y_SAFE_1 = 13
Y_SAFE_2 = 19

Z_SAFE_1 = 26
Z_SAFE_2 = 12

def main():

    # Start Print
    cnc = CNC.CNC(X_MOTOR_1, X_MOTOR_2, X_DIR, Y_MOTOR_1, Y_MOTOR_2, Y_DIR, Z_MOTOR_1, Z_MOTOR_2, Z_DIR, DRILL_PIN, CNC_WIDTH,CNC_HEIGHT, CNC_UNITS)

    gui = GUI.GUI(cnc)

    cnc.clean()

if __name__ == "__main__":
    main()