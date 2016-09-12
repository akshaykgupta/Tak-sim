import sys

class Game:

	class Player:

		def __init__(flats, capstones):
			self.flats = flats
			self.capstones = capstones

	def __init__(self, n):
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
		self.players.append(Player(self.max_flats, self.max_capstones))
		self.players.append(Player(self.max_flats, self.max_capstones))
		self.board = []
		for i in range(total_squares):
			self.board.append([])
		self.turn = 0
		self.max_down = 1
		self.max_up = n
		self.max_left = 'a'
		self.max_right = chr(ord('a') + n - 1)

	def execute_move(move_string):
		'''Return 1 on success, 0 on failure (invalid move)
		'''

		if self.turn == 0:
			self.moves += 1
		if self.moves != 1:
			current_piece = self.turn
		else:
			current_piece = 1 - self.turn
		if len(move_string) <= 0:
			return 0
		if move_string[0].isalpha():
			square = square_to_num(move_string[1:3])
			if square == -1:
				return 0
			if len(self.board[square]) != 0:
				return 0
			if move_string[0] == 'F' or move_string == 'S':
				if self.players[self.turn].flats == 0:
					return 0
				self.board[square].append((current_piece, move_string[0]))
				self.players[self.turn].flats -= 1
			elif move_string[0] == 'C':
				if self.players[self.turn].capstones == 0:
					return 0
				self.board[square].append((current_piece, move_string[0]))
				self.players[self.turn].capstones -= 1
			else:
				return 0
		elif move_string[0].isdigit():
			count = int(move_string[0])
			if count <= 0 or count > self.max_movable:
				return 0
			square = square_to_num(move_string[1:3])
			if square == -1:
				return 0
			if len(board[square]) < count:
				return 0
			direction = move_string[3]
			if direction == '+':
				change = 5
			elif direction == '-':
				change = -5
			elif direction == '>':
				change = 1
			elif direction == '<':
				change = -1
			else:
				return 0
			prev_square = square
			for i in range(4,len(move_string)):
				if not move_string[i].isdigit():
					return 0
				next_count = int(move_string[i])
				if next_count <= 0 or next_count > count:
					return 0
				next_square = prev_square + change
				if (next_square % n == 0 and prev_square % n == n - 1):
					return 0
				if (next_square % n == n - 1 and prev_square % n == 0):
					return 0
				if next_square >= self.total_squares or next_square < 0:
					return 0
				if len(board[next_square]) != 0 and board[next_square][-1][1] == 'S':
					if next_count != 1 or i != len(move_string) - 1:
						return 0
					if board[square][-1][1] != 'C':
						return 0
				if len(board[next_square]) != 0 and board[next_square][-1][1] == 'C':
					return 0
				count = count - next_count
				prev_square = next_square
			if count != 0:
				return 0
			count = int(move_string[0])
			prev_square = square
			for i in range(4, len(move_string)):
				next_count = int(move_string[i])
				next_square = prev_square + change
				if board[next_square][-1][1] == 'S':
					board[next_square][-1][1] == 'F'
				board[next_square] += board[square][-count:-count+next_count]
				prev_square = next_square
			board[square] = board[square][:-count]
		else:
			return 0
		return 1

	def square_to_num(square_string):
		''' Return -1 if square_string is invalid
		'''
		
		if len(square_string) != 2:
			return -1
		if not square_string[0].isalpha() or not square_string[1].isdigit():
			return -1
		row = ord(square_string[0])
		col = square_string[1]
		if row < 1 or row > self.n or col < 1 or col > self.n:
			return -1
		return self.n * (row - 1) + (col - 1)