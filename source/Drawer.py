import tkinter as tk
import DXF
import CNC
import ezdxf

class Drawer(object):

	def __init__(self, file, cnc):

		self.file = file
		self.cnc = cnc

		self.win = tk.Tk()

		self.RENDER_SIZE = 470

		self.win.minsize(680, 480)
		self.win.maxsize(800, 480)
		self.win.title("DXF Renderer")

		self.createGUI()

		# Open DXF file
		print(cnc.TABLE_WIDTH)
		self.dxf = DXF.DXF(file, cnc.TABLE_WIDTH, cnc.TABLE_HEIGHT, cnc.TABLE_UNITS)

		# Init UI with data from DXF file
		self.scaleBar.config(from_ = 0, to=len(self.dxf.ENTITIES), label="Total Operations - " + str(len(self.dxf.ENTITIES)))
		self.currentOp = 0

		self.drawDXF(0)

		self.win.mainloop()

	def createGUI(self):

		# ----- Init Window -----

		self.win.config(bg="#303030")

		# ----- Create Canvas -----

		self.canvas = tk.Canvas(self.win, height=self.RENDER_SIZE, width=470)
		self.canvas.pack(side=tk.LEFT, padx=5)

		# ----- Create Controls -----

		controlHolder = tk.Frame(self.win, bg="#404040")
		controlHolder.pack(expand=True, fill=tk.BOTH, padx = 5, pady=5)

		self.scaleBar = tk.Scale(controlHolder, length=172, label="Operations", orient=tk.HORIZONTAL, resolution=1, command=self.scaleMove, bg="#909090", fg="black", highlightbackground="#303030", troughcolor="#202020")
		self.scaleBar.pack(pady=(5, 0))

		buttonHolder = tk.Frame(controlHolder, bg="#606060")
		buttonHolder.pack(fill=tk.X, padx=5, pady=(5, 0))

		prevBtn = tk.Button(buttonHolder, text="Prev", bg="#909090", highlightbackground="#303030", activebackground="#202020", command=self.prev)
		prevBtn.pack(side=tk.LEFT, expand=True, pady=5)

		nextBtn = tk.Button(buttonHolder, text="Next", bg="#909090", highlightbackground="#303030", activebackground="#202020", command=self.next)
		nextBtn.pack(side=tk.LEFT, expand=True, pady=5)

		exitBtn = tk.Button(controlHolder, text="Exit", bg="#909090", highlightbackground="#303030", activebackground="#202020", command=self.win.destroy)
		exitBtn.pack(pady=(5, 0))

	def scaleMove(self, val):
		self.drawDXF(int(val))

	def next(self):

		if self.currentOp < len(self.dxf.ENTITIES):
			self.drawDXF(self.currentOp + 1)

	def prev(self):

		if self.currentOp > 0:
			self.drawDXF(self.currentOp - 1)

	def drawDXF(self, op):

		if op == self.currentOp:
			return

		self.currentOp = op

		# Update UI to show which operation currently displaying
		self.win.title("DXF Renderer - " + str(op) + "/" + str(len(self.dxf.ENTITIES)))
		self.scaleBar.set(op)
		self.canvas.delete("all")

		for x in range(0, op):
			self.drawEntity(self.dxf.ENTITIES[x])

	def drawEntity(self, e):

		if e.dxftype() == 'LINE':
			self.drawLine(e)
			return

		if e.dxftype() == 'ARC':
			self.drawArc(e)
			return

		print("Not supported: " + e.dxftype())

	def drawLine(self, e):

		startX = DXF.normalize(self.dxf.LENGTH_UNIT, self.dxf.TABLE_UNIT, self.dxf.TABLE_WIDTH, e.dxf.start[0])  * self.RENDER_SIZE
		startY = self.RENDER_SIZE - DXF.normalize(self.dxf.LENGTH_UNIT, self.dxf.TABLE_UNIT, self.dxf.TABLE_HEIGHT, e.dxf.start[1])  * self.RENDER_SIZE

		endX = DXF.normalize(self.dxf.LENGTH_UNIT, self.dxf.TABLE_UNIT, self.dxf.TABLE_WIDTH, e.dxf.end[0])  * self.RENDER_SIZE
		endY = self.RENDER_SIZE - DXF.normalize(self.dxf.LENGTH_UNIT, self.dxf.TABLE_UNIT, self.dxf.TABLE_HEIGHT, e.dxf.end[1])  * self.RENDER_SIZE

		self.canvas.create_line(startX, startY, endX, endY, width=1)

	def drawArc(self, e):

		radius = DXF.normalize(self.dxf.LENGTH_UNIT, self.dxf.TABLE_UNIT, self.dxf.TABLE_WIDTH, e.dxf.radius)  * self.RENDER_SIZE
		posX = DXF.normalize(self.dxf.LENGTH_UNIT, self.dxf.TABLE_UNIT, self.dxf.TABLE_WIDTH, e.dxf.center[0])  * self.RENDER_SIZE
		posY = self.RENDER_SIZE - DXF.normalize(self.dxf.LENGTH_UNIT, self.dxf.TABLE_UNIT, self.dxf.TABLE_WIDTH, e.dxf.center[1])  * self.RENDER_SIZE

		cord = (posX - radius, posY - radius, posX + radius, posY + radius)
		startAngle = e.dxf.start_angle
		extent = e.dxf.end_angle - startAngle

		self.canvas.create_arc(cord, start= startAngle, extent=extent, style=tk.ARC, width=1)







		