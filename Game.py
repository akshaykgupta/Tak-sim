import sys,pdb
from Board import Board
from Tkinter import *

class Game:

	# Constants
	SQUARE_SIZE = 80
	VER_SHIFT_MARGIN = 50
	HOR_SHIFT_MARGIN = 150
	COLOR_2 = '\033[91m'
	COLOR_1 = '\033[93m'
	COLOR_RC = '\033[96m'
	COLOR_END = '\033[0m'
	CELL_WIDTH = 15

	class Player:

		def __init__(self, flats, capstones):
			self.flats = flats
			self.capstones = capstones

	def __init__(self, n, mode):
		self.n = n
		self.moves = 0
		self.total_squares = n * n
		if n == 5:
			self.max_flats = 21
			self.max_capstones = 1
		elif n == 6:
			self.max_flats = 30
			self.max_capstones = 1
		elif n == 7:
			self.max_flats = 40
			self.max_capstones = 1
		else:
			raise ValueError('Board size is either 5, 6 or 7.')
		self.max_movable = n
		self.players = []
		self.players.append(Game.Player(self.max_flats, self.max_capstones))
		self.players.append(Game.Player(self.max_flats, self.max_capstones))
		self.board = []
		for i in xrange(self.total_squares):
			self.board.append([])
		self.turn = 0
		self.max_down = 1
		self.max_up = n
		self.max_left = 'a'
		self.max_right = chr(ord('a') + n - 1)
		self.winner = {}
		self.mode = mode
	
	def __str__(self):
		'''Returns a string representation of the current
		state of the game
		'''

		game_string = ''
		game_string += 'Current turn: Player ' + str(self.turn + 1) + '\n'
		game_string += 'Player 1 unplayed pieces: ' + str(self.players[0].flats) + \
					   'F, ' + str(self.players[0].capstones) + 'C\n'
		game_string += 'Player 2 unplayed pieces: ' + str(self.players[1].flats) + \
					   'F, ' + str(self.players[1].capstones) + 'C\n\n'
		for i in xrange(self.n-1, -1, -1):
			game_string += Game.COLOR_RC + str(i+1) + Game.COLOR_END + '  '
			for j in xrange(self.n):
				idx = i * self.n + j
				if len(self.board[idx]) == 0:
					for ii in xrange(Game.CELL_WIDTH):
						game_string += ' '
				else:
					spaces = (Game.CELL_WIDTH - len(self.board[idx])) / 2
					game_string += ' ' * spaces
					game_string += self.square_to_string(self.board[idx])
					spaces = (Game.CELL_WIDTH - len(self.board[idx]) + 1) / 2
					game_string += ' ' * spaces
			game_string += '\n'
		game_string += '   '
		for i in xrange(self.n):
			game_string += ' ' * (Game.CELL_WIDTH/2)
			game_string += Game.COLOR_RC + chr(i+97) + Game.COLOR_END
			game_string += ' ' * (Game.CELL_WIDTH/2)
		return game_string

	def square_to_string(self, square):
		square_string = ''
		for i in range(len(square)):
			if square[i][0] == 0:
				square_string += Game.COLOR_1
			else:
				square_string += Game.COLOR_2
			square_string += square[i][1]
			square_string += Game.COLOR_END
		return square_string

	def init_display(self):
		self.display = Tk()
		self.window_height = self.n * Board.SQUARE_SIZE + 2 * Board.VER_SHIFT_MARGIN
		self.window_width = self.n * Board.SQUARE_SIZE + 2 * Board.HOR_SHIFT_MARGIN
		self.canvas = Canvas(self.display, width = self.window_width, height = self.window_height, background = "#2c3e50")
		self.canvas.pack()
		self.render_board = Board(self.n, self.canvas, self.window_height, self.window_width)

	def render(self):
		print self.__str__()
		print '\n\n'

	def execute_move(self,move_string):
		'''Returns
		0 if move is invalid
		1 if move is valid
		2 if player 1 wins
		3 if player 2 wins
		'''
		move_string = move_string.strip()
		# pdb.set_trace()
		if self.turn == 0:
			self.moves += 1
		if self.moves != 1:
			current_piece = self.turn
		else:
			current_piece = 1 - self.turn
		if len(move_string) <= 0:
			return 0
		if move_string[0].isalpha():
			square = self.square_to_num(move_string[1:])
			if square == -1:
				return 0
			if len(self.board[square]) != 0:
				return 0
			if move_string[0] == 'F' or move_string[0] == 'S':
				if self.players[current_piece].flats == 0:
					return 0
				if self.moves == 1 and move_string[0] == 'S':
					return 0
				self.board[square].append((current_piece, move_string[0]))
				self.players[current_piece].flats -= 1
			elif move_string[0] == 'C':
				if self.moves == 1:
					return 0
				if self.players[current_piece].capstones == 0:
					return 0
				self.board[square].append((current_piece, move_string[0]))
				self.players[current_piece].capstones -= 1
			else:
				return 0
		elif move_string[0].isdigit():
			count = int(move_string[0])
			if count <= 0 or count > self.max_movable:
				return 0
			square = self.square_to_num(move_string[1:3])
			if square == -1:
				return 0
			if len(self.board[square]) < count:
				return 0
			direction = move_string[3]
			if direction == '+':
				change = self.n
			elif direction == '-':
				change = -self.n
			elif direction == '>':
				change = 1
			elif direction == '<':
				change = -1
			else:
				return 0
			prev_square = square
			for i in xrange(4,len(move_string)):
				if not move_string[i].isdigit():
					return 0
				next_count = int(move_string[i])
				if next_count <= 0 or next_count > count:
					return 0
				next_square = prev_square + change
				if (next_square % self.n == 0 and prev_square % self.n == self.n - 1):
					return 0
				if (next_square % self.n == self.n - 1 and prev_square % self.n == 0):
					return 0
				if next_square >= self.total_squares or next_square < 0:
					return 0
				if len(self.board[next_square]) != 0 and self.board[next_square][-1][1] == 'S':
					if next_count != 1 or i != len(move_string) - 1:
						return 0
					if self.board[square][-1][1] != 'C':
						return 0
				if len(self.board[next_square]) != 0 and self.board[next_square][-1][1] == 'C':
					return 0
				count = count - next_count
				prev_square = next_square
			if count != 0:
				return 0
			count = int(move_string[0])
			prev_square = square
			for i in xrange(4, len(move_string)):
				next_count = int(move_string[i])
				next_square = prev_square + change				
				if (len(self.board[next_square]) > 0) and (self.board[next_square][-1][1] == 'S'):
					self.board[next_square][-1] = (self.board[next_square][-1][0], 'F')
				if next_count - count == 0:
					self.board[next_square] += self.board[square][-count:]
				else:
					self.board[next_square] += self.board[square][-count:-count+next_count]
				prev_square = next_square
				count -= next_count
			count = int(move_string[0])
			self.board[square] = self.board[square][:-count]
		else:
			return 0
		winner = -1
		if self.check_road_win(self.turn):
			self.winner['player'] = self.turn
			self.winner['type'] = 'road'
			winner = 2 + self.turn
		elif self.check_road_win(1 - self.turn):
			self.winner['player'] = 1 - self.turn
			self.winner['type'] = 'road'
			winner = 3 - self.turn
		elif self.players[0].flats == 0 or self.players[1].flats == 0:
			winner = self.check_flat_win()
			self.winner['player'] = winner - 2
			self.winner['type'] = 'flat'
		self.turn = 1 - self.turn
		if self.mode == 'GUI':
			self.render_board.render(self)
		elif self.mode == 'CUI':
			self.render()
		if winner != -1:
			return winner
		return 1

	def square_to_num(self,square_string):
		''' Return -1 if square_string is invalid
		'''
		
		if len(square_string) != 2:
			return -1
		if not square_string[0].isalpha() or not square_string[0].islower() or not square_string[1].isdigit():
			return -1
		row = ord(square_string[0]) - 96
		col = int(square_string[1])
		if row < 1 or row > self.n or col < 1 or col > self.n:
			return -1
		return self.n * (col - 1) + (row - 1)

	def check_road_win(self, player):
		'''Checks for a road win for player
		'''

		def check_road_win(player, direction):
			'''Direction can be 'ver' or 'hor'
			'''
			visited = set()
			dfs_stack = []
			final_positions = set()
			if direction == 'ver':
				for i in xrange(self.n):
					if len(self.board[i]) > 0 and self.board[i][-1][0] == player and self.board[i][-1][1] != 'S':
						visited.add(i)
						dfs_stack.append(i)
					final_positions.add(self.total_squares - 1 - i)
			elif direction == 'hor':
				for i in xrange(self.n):
					if (len(self.board[i*self.n]) > 0) and (self.board[i*self.n][-1][0] == player) and (self.board[i*self.n][-1][1] != 'S'):
						visited.add(i*self.n)
						dfs_stack.append(i*self.n)
					final_positions.add((i + 1) * self.n - 1)
			while len(dfs_stack) > 0:
				square = dfs_stack.pop()
				if square in final_positions:
					return True
				nbrs = self.get_neighbours(square)
				for nbr in nbrs:
					if (nbr not in visited) and (len(self.board[nbr]) > 0) and (self.board[nbr][-1][0] == player) and (self.board[nbr][-1][1] != 'S'):
						dfs_stack.append(nbr)
						visited.add(nbr)
			return False

		return check_road_win(player, 'hor') or check_road_win(player, 'ver')

	def get_neighbours(self,square):
		'''Generate a list of neighbours for a given square
		Returns empty if square is invalid
		'''

		if isinstance(square, str):
			square = self.square_to_num(square)
		if square < 0 or square >= self.total_squares:
			return []
		elif square == 0:
			return [square+1, square+self.n]
		elif square == self.n - 1:
			return [square-1, square+self.n]
		elif square == self.total_squares - self.n:
			return [square+1, square-self.n]
		elif square == self.total_squares - 1:
			return [square-1, square-self.n]
		elif square < self.n:
			return [square-1, square+1, square+self.n]
		elif square % self.n == 0:
			return [square+1, square-self.n, square+self.n]
		elif (square + 1) % self.n == 0:
			return [square-1, square-self.n, square+self.n]
		elif square >= self.total_squares - self.n:
			return [square-1, square+1, square-self.n]
		else:
			return [square-1, square+1, square-self.n, square+self.n]

	def check_flat_win(self):
		'''Checks for a flat win
		'''

		count_1 = 0
		count_2 = 0
		for i in xrange(self.total_squares):
			if len(self.board[i]) > 0 and self.board[i][-1][0] == 0 and self.board[i][-1][1] != 'S':
				count_1 += 1
			elif len(self.board[i]) > 0 and self.board[i][-1][0] == 1 and self.board[i][-1][1] != 'S':
				count_2 += 1
		if count_1 > count_2:
			return 2
		elif count_2 > count_1:
			return 3
		elif self.players[0].flats == 0:
			return 3
		elif self.players[1].flats == 0:
			return 2

	def calculate_score(self, player):
		'''Calculates the score of the player
		'''
		if 'player' not in self.winner:
			raise ValueError('Nobody has won yet.')
		count_1 = 0
		count_2 = 0
		for i in xrange(total_squares):
			if len(self.board[i]) > 0 and self.board[i][-1][0] == 0 and self.board[i][-1][1] != 'S':
				count_1 += 1
			elif len(self.board[i]) > 0 and self.board[i][-1][0] == 1 and self.board[i][-1][1] != 'S':
				count_2 += 1
		if player != self.winner['player'] and player == 0:
			return count_1
		elif player != self.winner['player'] and player == 1:
			return count_2
		if self.winner['type'] == 'road':
			return self.players[player].flats + self.total_squares
		elif self.winner['type'] == 'flat':
			if player == 0:
				return self.players[player].flats + count_1
			elif player == 1:
				return self.players[player].flats + count_2

