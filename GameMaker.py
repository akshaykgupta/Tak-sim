import sys
f = open(sys.argv[1])
g = open('blackMoves.txt','w')
h = open('whiteMoves.txt','w')
def convertMove(move):
	if(move[0].isalpha() and move[0].islower()):
		move = 'F' + move
	return move
for line in f:
	if(line.startswith('[')):
		continue
	line = line.strip()
	if(line == ''):
		continue
	line = line.split()
	move1 = convertMove(line[1])
	move2 = convertMove(line[2])
	h.write(move1+'\n')
	g.write(move2+'\n')
