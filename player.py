import sys
import pdb
data = sys.stdin.readline()
moveFile = None
player = -1
allMoves = None

if(data == 'Player 1'):
	player = 1
	moveFile = open('whiteMoves.txt','rb')
	allMoves = moveFile.readlines()
else:
	player = 2
	moveFile = open('blackMoves.txt','rb')
	allMoves = moveFile.readlines()
if(player == 1):
	idx = 0
	while True:		
		move = allMoves[idx].strip()
		# Write move to client
		sys.stdout.write(move + "\n")		
		# read move from client
		move = sys.stdin.readline()
		idx += 1
		if(idx == len(allMoves)):
			break
elif(player == 2):
	idx = 0
	while True:		
		# read move from client
		move = sys.stdin.readline()		
		move = allMoves[idx].strip()
		#Send move from client
		sys.stdout.write(move + "\n")
		idx += 1
		if(idx == len(allMoves)):
			break