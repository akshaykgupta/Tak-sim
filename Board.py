import sys, time, socket
from Tkinter import *
import math

class Board:
	#CONSTANTS
	SQUARE_SIZE = 70
	FLAT_SIZE = 50
	CAP_DIAMETER = 40
	SHIFT_MARGIN = 20
	BOTTOM_LABEL_X = 10
	BOTTOM_LABEL_Y = 20
	SIDE_LABEL_X = 20
	SIDE_LABEL_Y = 10
	LABEL_SPACING = 70
	LABEL_FONT_SIZE = 20

	def __init__(self, n):
		if self.display:
			display.destroy()
		self.n = n
		self.display = Tk()
		self.window_height = n * SQUARE_SIZE + 2 * SHIFT_MARGIN
		self.window_width = n * SQUARE_SIZE + 2 * SHIFT_MARGIN
		self.canvas = Canvas(self.display, width = self.window_width, height = self.window_height)
		self.canvas.pack()
		self.draw_squares()
		self.draw_tiles()