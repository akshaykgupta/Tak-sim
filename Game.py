import sys

class Game:

	class Player:

		def __init__(self, flats, capstones):
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
		self.players.append(Game.Player(self.max_flats, self.max_capstones))
		self.players.append(Game.Player(self.max_flats, self.max_capstones))
		self.board = []
		for i in range(self.total_squares):
			self.board.append([])
		self.turn = 0
		self.max_down = 1
		self.max_up = n
		self.max_left = 'a'
		self.max_right = chr(ord('a') + n - 1)

	def execute_move(move_string):
		'''Returns
		0 if move is invalid
		1 if move is valid
		2 if player 1 wins
		3 if player 2 wins
		'''

		move_string = move_string.strip()
		if self.turn == 0:
			self.moves += 1
		if self.moves != 1:
			current_piece = self.turn
		else:
			current_piece = 1 - self.turn
		if len(move_string) <= 0:
			return 0
		if move_string[0].isalpha():
			square = square_to_num(move_string[1:])
			if square == -1:
				return 0
			if len(self.board[square]) != 0:
				return 0
			if move_string[0] == 'F' or move_string[0] == 'S':
				if self.players[current_piece].flats == 0:
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
			square = square_to_num(move_string[1:3])
			if square == -1:
				return 0
			if len(board[square]) < count:
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
			for i in range(4,len(move_string)):
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
					board[next_square][-1] = (board[next_square][-1][0], 'F')
				if next_count - count == 0:
					board[next_square] += board[square][-count:]
				else:
					board[next_square] += board[square][-count:-count+next_count]
				prev_square = next_square
				count -= next_count
			count = int(move_string[0])
			board[square] = board[square][:-count]
		else:
			return 0
		if self.check_win(self.turn):
			return 2 + self.turn
		if self.check_win(1 - self.turn):
			return 3 - self.turn
		self.turn = 1 - self.turn
		return 1

	def square_to_num(square_string):
		''' Return -1 if square_string is invalid
		'''
		
		if len(square_string) != 2:
			return -1
		if not square_string[0].isalpha() or not square_string[0].islower() or not square_string[1].isdigit():
			return -1
		row = ord(square_string[0]) - 96
		col = square_string[1]
		if row < 1 or row > self.n or col < 1 or col > self.n:
			return -1
		return self.n * (col - 1) + (row - 1)

	def check_win(player):
		'''Checks whether player has won the game
		'''

		def check_win(player, direction):
			'''Direction can be 'ver' or 'hor'
			'''
			visited = set()
			dfs_stack = []
			final_positions = set()
			if direction == 'ver':
				for i in range(self.n):
					if len(self.board[i]) > 0 and self.board[i][-1][0] == player:
						visited.add(i)
						dfs_stack.append(i)
					final_positions.add(self.total_squares - 1 - i)
			elif direction == 'hor':
				for i in range(self.n):
					if len(self.board[i*self.n]) > 0 and self.board[i*self.n][-1][0] == player:
						visited.add(i)
						dfs_stack.add(i)
					final_positions.add((i + 1) * self.n - 1)
			while len(dfs_stack) > 0:
				square = dfs_stack.pop()
				if square in final_positions:
					return True
				nbrs = self.get_neighbours(square)
				for nbr in nbrs:
					if nbr not in visited and len(self.board[nbr]) > 0 and self.board[nbr][-1][0] == player:
						dfs_stack.add(nbr)
						visited.add(nbr)
			return False

		return check_win(player, 'hor') or check_win(player, 'ver')

	def get_neighbours(square):
		'''Generate a list of neighbours for a given square
		Returns empty if square is invalid
		'''

		if isinstance(square, str):
			square = self.square_to_num(square)
		if square < 0 or square > self.total_squares:
			return []
		elif square == 0:
			return [square+1, square+self.n]
		elif square == self.n - 1:
			return [square-1, square+self.n]
		elif square == self.total_squares - self.n - 1:
			return [square+1, square-self.n]
		elif square == self.total_squares:
			return [square-1, square-self.n]
		elif square < self.n:
			return [square-1, square+1, square+self.n]
		elif square % self.n == 0:
			return [square+1, square-self.n, square+self.n]
		elif (square + 1) % self.n == 0:
			return [square-1, square-self.n, square+self.n]
		elif square > total_squares - self.n:
			return [square-1, square+1, square-self.n]
		else:
			return [square-1, square+1, square-self.n, square+self.n]

