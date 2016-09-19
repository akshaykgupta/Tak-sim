import sys
import pdb
import time
data = sys.stdin.readline().strip()
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
		time.sleep(1)		
		move = allMoves[idx].strip()
		# Write move to client		
		move = move + '\n'		
		sys.stdout.write(move)
		sys.stdout.flush()
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
		time.sleep(1)
		move = allMoves[idx].strip()
		#Send move from client
		sys.stdout.write(move + "\n")
		sys.stdout.flush()
		idx += 1
		if(idx == len(allMoves)):
			break