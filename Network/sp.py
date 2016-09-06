import sys
counter = 0
while counter < 100:	
	data = sys.stdin.readline()		
	data = data.strip()
	# sys.stderr.write("Child Received " + data + "\n")
	counter = int(data) + 1
	sys.stdout.write(str(counter) + "\n")
	sys.stdout.flush()
	





