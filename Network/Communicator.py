import socket,sys
from subprocess import Popen, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR

class Communicator(object):
	def __init__(self): 
		self.Socket = None
		self.ChildProcess = None		

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
				# -- TODO: Handle connection Timeout (Check Signal Setting in Python)--- #
				data = self.Socket.recv(1024)
				if(len(data) <= 0):
					continue
				return data
	def CreateChildProcess(self,Execution_Command,Executable_File):		
		self.ChildProcess = Popen ([Execution_Command, Executable_File], stdin = PIPE, stdout = PIPE, bufsize=0)
		self.ModifiedOutStream = NBSR(self.ChildProcess.stdout)		
		

	def RecvDataOnPipe(self,TIMEOUT):
		data = None
		if(self.isChildProcessNotNone()):
			try:
				data = self.ModifiedOutStream.readline(TIMEOUT)
			except:
				pass
		return data
						
	def SendDataOnPipe(self,data):
		success_flag = False
		if(self.isChildProcessNotNone()):
			try:
				self.ChildProcess.stdin.write(data)
				success_flag = True
			except:
				success_flag = False
		return success_flag
	
	def closeChildProcess(self):
		if(self.isChildProcessNotNone()):			
			self.ChildProcess.kill()
			self.ChildProcess = None
		

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

	

	
	
	