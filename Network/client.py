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
		""" Checks the Existance of the Executable File and
			if the extension of the file matches the command used to run it
		Args:
			Execution_Command : Command used to execute the Executable File (sh, python ./ etc)
			Executable_File : The Executable File
		Returns: 
			None			
		 """
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
		""" Creates a Process, with which the client communicates.
			Checks the existance of the Executable_File and some basic
			checks for whether the Execution_Command used to run the code
			matches the extension of the Executable File
			Prints if error is found
		Args:
			Execution_Command : Command used to execute the Executable File (sh, python ./ etc)
			Executable_File : The Executable File
		Returns: 
			None
		"""
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
		""" Sends Data to the Server as a json object of the following format.
		{
			meta : '' / MetaData in case of an Error
			action : 'NORMAL' / 'KILLPROC' in case of an Error
			data : 'DATA' / '' in case of an Error 
		} 
		Args:
			data : The data to be sent to the server. This can be: 
						A move, which would be a string 
						'' in case of an ERROR (wrong move, Timeout etc)
			ErrorMeta : The meta data of the Error ( UNEXPECTED STOP, WRONG MOVE etc.)
		Returns:
			None 
		"""
		#TODO : Implement a flag, similar to SendData2Process, to denote success and failure
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
		""" Receives data from the Server as a string, and Returns the Data.
			In case of an error, prints the error, and closes the pipe process
		Args:
			None
		Returns:
			retData : String in case there are no errors, otherwise None
		"""		
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
		"""
			Receives Data from the process. This does not implement checks 
			on the validity of game moves. Hence, the retData from here is not final
			, i.e, it may be different than what is sent to the server.
			Handles Errors like Exceptions thrown by process. 
			Uses self.TIMER to decide how long to wait for a timeout.
			For both the above cases, prints the error msg and closes the connection to 
			the process. 
		Args:
			None
		Returns:
			retData : JSON DUMP (string, loaded with json.loads(string_name))
					  of the nature : 
					  {
							meta : '' / MetaData in case of an Error
							action : 'NORMAL' / 'KILLPROC' in case of an Error
							data : 'DATA' / '' in case of an Error 
						}
		"""
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
		""" Sends Data to the process. Handles the case if the process being communicated to has closed.
		Args: 
			data : string data, to send the process (a game move)
		Returns:
			success_flag : A boolean flag to denote the data transfer to the process was successful or not.
		"""
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



	

