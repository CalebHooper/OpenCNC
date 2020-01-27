import turtle
import DXF
import ezdxf
import numpy




class Renderer:

    def __init__(self, nDXF, winWidth, winHeight):
        self.model = nDXF

        self.WIDTH = winWidth
        self.HEIGHT = winHeight

        self.window = turtle.Screen()
        self.window.setup(width=self.WIDTH, height=self.HEIGHT)

        turtle.speed(10)

    def startDrawing(self):

        # Loop through shapes in model
        for e in self.model.ENTITIES:

            self.drawShape(e)

        self.window.exitonclick()

    def drawShape(self, e):

        if e.dxftype() == 'LINE':
            self.drawLine(e)
            return

        if e.dxftype() == 'ARC':
            self.drawArc(e)
            return

        print(e.dxftype() + " HAS NOT BEEN IMPLMENTED")


            


    def drawLine(self, e):
        
        # Move pen to start of line
        turtle.penup()
        posX = DXF.normalize(self.model.LENGTH_UNIT, self.model.TABLE_UNIT, self.model.TABLE_WIDTH, e.dxf.start[0])  * self.WIDTH - (self.WIDTH / 2)
        posY = DXF.normalize(self.model.LENGTH_UNIT, self.model.TABLE_UNIT, self.model.TABLE_HEIGHT, e.dxf.start[1])  * self.HEIGHT - (self.HEIGHT / 2)
        turtle.setpos(posX, posY)
        turtle.pendown()

        # Rotate pen towards end of line
        deltaX = e.dxf.end[0] - e.dxf.start[0]
        deltaY = e.dxf.end[1] - e.dxf.start[1]
        rad = numpy.arctan2(deltaY, deltaX)
        deg = rad * (180.0 / 3.14159)
        turtle.setheading(deg)

        # Move pen length of line
        dist = numpy.sqrt(deltaX * deltaX + deltaY * deltaY)
        dist = DXF.normalize(self.model.LENGTH_UNIT, self.model.TABLE_UNIT, self.model.TABLE_WIDTH, dist)

        turtle.forward(dist * self.WIDTH)

    def drawArc(self, e):

        turtle.penup()

        posX = DXF.normalize(self.model.LENGTH_UNIT, self.model.TABLE_UNIT, self.model.TABLE_WIDTH, e.dxf.center[0]) * self.WIDTH - (self.WIDTH / 2)
        posY = DXF.normalize(self.model.LENGTH_UNIT, self.model.TABLE_UNIT, self.model.TABLE_HEIGHT, e.dxf.center[1]) * self.HEIGHT - (self.HEIGHT / 2)
        turtle.setpos(posX, posY)

        turtle.pendown()

        radius = DXF.normalize(self.model.LENGTH_UNIT, self.model.TABLE_UNIT, self.model.TABLE_WIDTH, e.dxf.radius) * self.WIDTH

        turtle.setheading(0)

        turtle.circle(radius)







