import socket,sys
from subprocess import Popen, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR

# TODO : Move constants to another file
SAFETY_TIMEOUT = 15
class Communicator:
	def __init__(self): 
		self.Socket = None
		self.ChildProcess = None
		self.Timer = None   # Game Timer

	def setSocket(self,Socket):
		self.Socket = Socket

	def isSocketNotNone(self):
		if(self.Socket is None):
			return False
		else:
			return True

	def isChildProcessNotNone(self):
		if(self.ChildProcess is None):
			return False
		else:
			return True
	
	def closeSocket(self):
		if(self.isSocketNotNone()):
			self.Socket.close()
			self.Socket = None

	def SendDataOnSocket(self,data):
		if(self.isSocketNotNone()):
			self.Socket.send(data)

	def RecvDataOnSocket(self):
		if(self.isSocketNotNone()):
			data = None
			while True:
				# -- Handle connection Timeout (Check Signal Setting in Python)--- #
				data = self.Socket.recv(1024)
				if(len(data) <= 0):
					continue
				return data
	def CreateChildProcess(self,Execution_Command,Executable_File):
		# TODO: Check existance of Executable_File and match Extension with Execution_Command
		self.ChildProcess = Popen ([Execution_Command, Executable_File], stdin = PIPE, stdout = PIPE, bufsize=0)
		self.ModifiedOutStream = NBSR(self.ChildProcess.stdout)		
		

	def RecvDataOnPipe(self):
		data = None
		if(self.isChildProcessNotNone()):
			try:
				data = self.ModifiedOutStream.readline(SAFETY_TIMEOUT)
			except:
				print 'Something Bad Happened'
		return data
						
	def SendDataOnPipe(self,data):
		if(self.isChildProcessNotNone()):
			try:
				self.ChildProcess.stdin.write(data)				
			except:
				print 'Something Bad Happened'
	def closeChildProcess(self):
		if(self.isChildProcessNotNone()):
			self.ChildProcess.kill()
		

if __name__ == '__main__':
	c = Communicator()
	c.CreateChildProcess('sh','run.sh')
	counter = 1
	try:
		while(counter != 100):
			c.SendDataOnPipe(str(counter) + '\n')
			data = c.RecvDataOnPipe()		
			print "Parent Recieved",data
			data = data.strip()
			counter = int(data)
	except:
		c.closeChildProcess()

	

	
	
	