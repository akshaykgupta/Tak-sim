from Communicator import Communicator
import socket,sys,json,os,time
import math

class Client(Communicator):
	def __init__(self):
		self.GAME_TIMER = 15000 # in Milli Seconds
		self.NETWORK_TIMER = 60		
		super(Client,self).__init__()
		pass	
	
	def setNetworkTimer(self,Time_in_Seconds):
		self.NETWORK_TIMER = Time_in_Seconds
	
	def getNetworkTimer(self):
		return self.NETWORK_TIMER

	def getGameTimer(self):
		return self.GAME_TIMER
	
	def setGameTimer(self,Time_in_Seconds):
		self.GAME_TIMER = Time_in_Seconds

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
		"""Connects to server with given IP Address and Port No. 
		Args: 
			server_address : IP Address
			Port No : Port Number
		Returns: 
			None
		"""				
		self.clientSocket = socket.socket()
		self.clientSocket.connect((server_address,port_no))		
		super(Client,self).setSocket(self.clientSocket)
		
		

	def SendData2Server(self,data):		
		""" Sends data (a dictionary) to the Server as a json object
		In case action == 'FINISH', closes the pipe on this end
		Args:
			data : a dictionary of the following format:
			{
				meta : The meta data in case of an error ( UNEXPECTED STOP, WRONG MOVE etc.), otherwise ''	
				action : The action to be taken (KILLPROC, NORMAL, FINISH)
				data : Move String or '' in case of an Error
			}
		Returns:			
			success_flag : True if successful in sending, False otherwise
		"""				
		if((data['action'] == 'KILLPROC') or (data['action'] == 'FINISH')):
			super(Client,self).closeChildProcess()		
		
		sendDat = json.dumps(data)
		success_flag =  super(Client,self).SendDataOnSocket(sendData)
		if(not success_flag):
			print 'ERROR : FAILED TO SEND DATA TO SERVER'
			super(Client,self).closeSocket()
		return success_flag

	
	def RecvDataFromServer(self):
		""" Receives data from the Server as a string, and Returns the Move.
			Uses self.NETWORK_TIMER to decide how long to wait for input from Server
			In case of an error, prints the error, and closes the pipe process
			In case the last move is made by other client, closes the pipe process and 
			returns the data
		Args:
			None
		Returns:
			retData : String (Move) in case there are no errors, otherwise None
		"""		
		data = super(Client,self).RecvDataOnSocket(self.NETWORK_TIMER)
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
			elif(data['action'] == 'FINISH'):
				super(Client,self).closeChildProcess()				
				retData = data['data']
		return retData
	
	def RecvDataFromProcess(self):
		"""Receives Data from the process. This does not implement checks 
			on the validity of game moves. Hence, the retData from here is not final
			, i.e, it may be different than what is sent to the server.
			Note: The Action 'FINISH' is set internally by game, not by the network
			Handles Errors like Exceptions thrown by process. 
			However, In case of a timeout, 'FINISH' may be thrown
			Uses self.GAME_TIMER to decide how long to wait for a timeout.
			For both the above cases, prints the error msg and closes the connection to 
			the process. 
		Args:
			None
		Returns:
			retData : dictionary of the nature : 
					  {
							meta : '' / MetaData in case of an Error
							action : 'NORMAL' / 'KILLPROC' in case of an Error
							data : 'DATA' / '' in case of an Error 
						}
					  None in case of an error
		"""		
		start_time = time.time()
		BUFFER_TIMER = math.ceil(self.GAME_TIMER / 1000.0)
		data = super(Client,self).RecvDataOnPipe(BUFFER_TIMER)
		end_time = time.time()
		retData = None		
		if(data == None):								
			print 'ERROR : THIS CLIENT STOPPED UNEXPECTEDLY OR TIMED OUT'
			super(Client,self).closeChildProcess()			
			retData = {'meta':'UNEXPECTED STOP','action':'KILLPROC','data':''}
		else:			
			# 1 Milli Second Default
			time_delta = max(1,int((end_time - start_time) * 1000))
			self.GAME_TIMER -= time_delta
			if(self.GAME_TIMER > 0):
				retData = {'meta':'','action':'NORMAL','data':data}
			else:
				retData = {'meta':'TIMEOUT','action':'FINISH','data':data}				
		return retData
	
	
	def SendData2Process(self,data):
		""" Sends Data (Move) to the process. Handles the case if the process being communicated with has closed.
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



	

