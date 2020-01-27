import sys
import FileReader
import DXF
import Renderer
import CNC
import time
import GUI

# Global Variables
VERIFY_WINDOW_SIZE = 1000


def main():
    # Load DXF File To Print
    #model = DXF.DXF(FileReader.loadDXF(), 20, 20, DXF.INCHES)

    # Create Render Of Print
    #renderer = Renderer.Renderer(model, 1000, 1000)
    #renderer.startDrawing()

    # Ask For User Confrimation

    # Start Print
    cnc = CNC.CNC(0, 0, 0, 0, 0, 0, 21)
    cnc.startDrill(.5, .5)

    gui = GUI.GUI(cnc)
    #
    #time.sleep(3)
    #cnc.stopDrilling()

    while True:
        i = 0

    

if __name__ == "__main__":
    main()