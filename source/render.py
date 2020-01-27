import ezdxf
import turtle 
import numpy

# Nomralize A Value To Fit 20x20 Inch CNC router
def normalize(val):

    global UNIT_LENGTH

    # If Inches
    if UNIT_LENGTH == 1:
        return val / 20.0

    # If Feet

    # If Centimeters

    # If Meters

    # If Mili-Meters


def drawLine(START, END):

    global SCREEN_SIZE

    # Place Turtle At Start Of Line
    turtle.penup()

    turtle.setx(normalize(START[0]) * SCREEN_SIZE - SCREEN_SIZE / 2)
    turtle.sety(normalize(START[1]) * SCREEN_SIZE - SCREEN_SIZE / 2)

    turtle.pendown()

    # Rotate To Correct Direction
    deltaX = END[0] - START[0]
    deltaY = END[1] - START[1]
    rad = numpy.arctan2(deltaY, deltaX)
    deg = rad * (180.0 / 3.14159)

    turtle.setheading(deg)


    # Clacalte Distance To Move
    distY = END[1] - START[1]
    distX = END[0] - START[0]

    dist = numpy.sqrt(distX * distX + distY * distY)
    dist = normalize(dist)

    turtle.forward(dist * SCREEN_SIZE)

def drawArc(CENTER, RADIUS, START_ANGLE, END_ANGLE):

    global SCREEN_SIZE

    turtle.penup()
    turtle.setx(CENTER[0])
    turtle.sety(CENTER[1])
    turtle.pendown()

    turtle.circle(normalize(RADIUS) * SCREEN_SIZE, END_ANGLE - START_ANGLE)


def renderDXF(DXF, SIZE):

    # Get Units Of File
    global UNIT_LENGTH  
    global UNIT_ANGLE   
    global SCREEN_SIZE
    SCREEN_SIZE = SIZE
    UNIT_LENGTH = DXF.header['$INSUNITS']
    UNIT_ANGLE  = DXF.header['$AUNITS']

    # Create Window
    window = turtle.Screen()
    window.setup(width=SIZE, height=SIZE)
    turtle.bgcolor("white")
    turtle.pensize(3)


    turtle.setx(0)
    turtle.sety(0)
    turtle.setheading(45)

    turtle.circle(100)

    return
    

    MSP = DXF.modelspace()

    # Loop Through All Shapes
    for e in MSP:
        
        if e.dxftype() == 'LINE':
            drawLine(e.dxf.start, e.dxf.end)
        if e.dxftype() == 'ARC':
            drawArc(e.dxf.center, e.dxf.radius, e.dxf.start_angle, e.dxf.end_angle)


        # Draw Shapes

    window.exitonclick()


