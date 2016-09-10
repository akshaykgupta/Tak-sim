from Communicator import Communicator
import socket,sys,json,os


class Client(Communicator):
	def __init__(self):
		self.TIMER = 15
		super(Client,self).__init__()
		pass	
	
	def getTimer(self):
		return self.TIMER
	
	def setTimer(self,Time_in_Seconds):
		self.TIMER = Time_in_Seconds

	def CheckExeFile(self,Execution_Command,Executable_File):
		print Executable_File
		Extension = Executable_File.split('.')
		if(len(Extension) == 1):
			return False
		Extension = Extension[-1]
		if(os.path.isfile(Executable_File)):
			if(Execution_Command == './' or Execution_Command == 'sh'):
				if(Extension == 'sh' or Extension == 'o'):
					return True
				else:
					return False
			elif(Execution_Command == 'java'):
				if(Extension == 'java'):
					return True
				else:
					return False
			elif(Execution_Command == 'python'):
				if(Extension == 'py'):
					return True
				else:
					return False
		else:
			return False
	
	def CreateChildProcess(self,Execution_Command,Executable_File):
		if(self.CheckExeFile(Execution_Command,Executable_File)):
			super(Client,self).CreateChildProcess(Execution_Command,Executable_File)
		else:
			print 'ERROR : EITHER FILE ', Executable_File,' DOES NOT EXIST',
			print 'OR THE EXECUTION COMMAND TO RUN THE FILE ',Execution_Command,' IS INCORRECT'			

	def Connect2Server(self,server_address,port_no):
		self.clientSocket = socket.socket()
		self.clientSocket.connect((server_address,port_no))		
		super(Client,self).setSocket(self.clientSocket)

	def SendData2Server(self,data,ErrorMeta = ''):
		sendData = None
		action = ''
		if(ErrorMeta == ''):
			assert(data == '')
			action = 'KILLPROC'
		else:			
			assert(ErrorMeta == '')
			action = 'NORMAL'								
		
		sendDat = json.dumps({'meta':ErrorMeta,'action':action,'data':data})
		super(Client,self).SendDataOnSocket(sendData)

	def RecvDataFromServer(self):		
		data = super(Client,self).RecvDataOnSocket()
		retData = None
		if(data == None):			
			print 'ERROR : TIMEOUT ON SERVER END'
			super(Client,self).closeChildProcess()
			super(Client,self).closeSocket()
		else:
			data = json.loads(data)
			if(data['action'] == 'NORMAL'):
				retData = data['data']
			elif(data['action'] == 'KILLPROC'):
				print 'ERROR : ' + data['meta'] + ' ON OTHER CLIENT'
				super(Client,self).closeChildProcess()
				super(Client,self).closeSocket()				
		return retData
	
	def RecvDataFromProcess(self):
		'''
			This does not implement checks on the validity of game moves
			Hence, the retData from here is not final, i.e, 
			it may be different than what is sent to the server

		'''
		data = super(Client,self).RecvDataOnPipe(self.TIMER)
		retData = None		
		if(data == None):								
			print 'ERROR : THIS CLIENT STOPPED UNEXPECTEDLY'
			super(Client,self).closeChildProcess()
			retData = json.dumps({'meta':'UNEXPECTED STOP','action':'KILLPROC','data':''})
		else:
			retData = json.dumps({'meta':'','action':'NORMAL','data':data})
		return retData
	
	def SendData2Process(self,data):
		success_flag = super(Client, self).SendDataOnPipe(data)
		if(success_flag == False):
			print 'ERROR : FAILED TO SEND DATA TO PROCESS'
			super(Client,self).closeChildProcess()
		return success_flag


if __name__ == '__main__':
	client = Client()
	client.Connect2Server(sys.argv[1],int(sys.argv[2]))
	if(int(sys.argv[5]) == 1):
		client.CreateChildProcess('sh','run.sh')
		counter = 0;
	else: 
		client.CreateChildProcess(sys.argv[3],sys.argv[4])
		counter = int(client.RecvDataFromServer())
	# try:
	while(counter < 100):
		client.SendData2Process(str(counter) + '\n')
		data = client.RecvDataOnPipe().strip()		
		print 'Client Recieved Data From Process ', data
		client.SendData2Server(data)
		data = client.RecvDataFromServer()
		print 'Client Recieved Data From Server ',data
		counter = int(data)		
	# except:
		# client.closeSocket()
	client.SendDataOnPipe(str(counter) + '\n')
	client.closeChildProcess()
	client.closeSocket()



	

