import sys, time, socket
from Tkinter import *
from threading import Thread
import math

class Board(object):
	#CONSTANTS
	SQUARE_SIZE = 80
	FLAT_SIZE = 30
	CAP_RADIUS = 12
	VER_SHIFT_MARGIN = 50
	HOR_SHIFT_MARGIN = 150
	BOTTOM_LABEL_X = 135
	BOTTOM_LABEL_Y = 90
	SIDE_LABEL_X = 190
	SIDE_LABEL_Y = 465
	FONT_SIZE = 20

	def __init__(self, n):		
		self.n = n
		self.display = Tk()
		Board.SIDE_LABEL_Y = n * Board.SQUARE_SIZE + 65
		self.window_height = n * Board.SQUARE_SIZE + 2 * Board.VER_SHIFT_MARGIN
		self.window_width = n * Board.SQUARE_SIZE + 2 * Board.HOR_SHIFT_MARGIN
		self.canvas = Canvas(self.display, width = self.window_width, height = self.window_height)
		self.canvas.pack()		
		self.squares = [[ [] for i in xrange(n)] for ii in xrange(n)]		
		Th = Thread(target = lambda : self.background_loop())
		Th.start()
		self.display.mainloop()
	
	def background_loop(self):
		self.draw_squares()
		self.draw_board_labels()
		board_list = [[] for idx in xrange(self.n*self.n)]
		board_list[7] = [(1,'F'), (0, 'F'), (0, 'F'), (1, 'F'), (0, 'F'), (1,'F'),(1,'F'),(1,'F'),(0,'F'),(1,'F'),(1,'C')]
		self.draw_tiles(board_list)

	def draw_board_labels(self):
		x = Board.BOTTOM_LABEL_X
		for i in xrange(self.n):
			y = Board.BOTTOM_LABEL_Y + i * Board.SQUARE_SIZE
			l = self.canvas.create_text((x, y), text = str(self.n - i), font = ("Arial", self.FONT_SIZE), fill = "#e74c3c")
		y = Board.SIDE_LABEL_Y
		for i in xrange(self.n):
			x = Board.SIDE_LABEL_X + i * Board.SQUARE_SIZE
			l = self.canvas.create_text((x, y), text = chr(i + 97), font = ("Arial", self.FONT_SIZE), fill = "#e74c3c")

	def draw_tiles(self, board_list):
		for r in xrange(self.n):
			for c in xrange(self.n):
				idx = (self.n - 1 - r) * self.n + c
				x_origin = Board.HOR_SHIFT_MARGIN + c*Board.SQUARE_SIZE + 25
				y_origin = Board.VER_SHIFT_MARGIN + r*Board.SQUARE_SIZE + 25
				if (len(board_list[idx]) > 1) and (board_list[idx][-1][1] == 'S' or board_list[idx][-1][1] == 'C'):
					y_origin += min ((len(board_list[idx]) - 2) * 5, 20)
				else:
					y_origin += min( (len(board_list[idx]) - 1)*5, 20)
				for i, elem in enumerate(board_list[idx]):
					if elem[1] == 'F':
						self.draw_flat(elem, x_origin, y_origin - i*5)
					elif elem[1] == 'S':
						self.draw_wall(elem, x_origin + Board.FLAT_SIZE/2, y_origin + Board.FLAT_SIZE/2 - max(0, i-1)*5)
					elif elem[1] == 'C':
						self.draw_capstone(elem, x_origin + Board.FLAT_SIZE/2, y_origin + Board.FLAT_SIZE/2 - max(0, i-1)*5)

	def draw_flat(self, elem, x, y):		
		fill = ["#FFFFFF", "#000000"]
		self.canvas.create_rectangle(x, y, x + Board.FLAT_SIZE, y + Board.FLAT_SIZE, fill = fill[elem[0]], outline = "#e74c3c")

	def draw_capstone(self, elem, x, y):
		
		fill = ["#FFFFFF", "#000000"]
		r = Board.CAP_RADIUS
		self.canvas.create_oval(x - r, y - r, x + r, y + r, fill = fill[elem[0]], outline = "#e74c3c")

	def draw_wall(self, elem, x, y):
		pass

	def draw_squares(self):
		for r in xrange(self.n):
			for c in xrange(self.n):
				x = Board.HOR_SHIFT_MARGIN + (c * Board.SQUARE_SIZE )
				y = Board.VER_SHIFT_MARGIN + (r * Board.SQUARE_SIZE)
				sq = self.canvas.create_rectangle(x,y , x + Board.SQUARE_SIZE, y + Board.SQUARE_SIZE, fill = "#4cf3d2")
				self.squares[r][c] = sq

if __name__ == "__main__":
	b = Board(5)
