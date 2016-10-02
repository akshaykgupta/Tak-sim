import sys, pdb
f = open(sys.argv[1])
g = open('blackMoves_draw.txt','w')
h = open('whiteMoves_draw.txt','w')
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
	if(len(line) > 2):
		move2 = convertMove(line[2])
	else:
		move2 = None
	h.write(move1+'\n')
	if not move2 is None:
		g.write(move2+'\n')
