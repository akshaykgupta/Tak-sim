import socket,sys,json
from Communicator import Communicator

class Server:
	def __init__(self):
		"""	
			Constructor. Initializes the communicator_list to [] and the NETWORK_TIMER to 60
		Args:
			None
		Returns:
			None
		"""
		self.communicator_list = []
		self.NETWORK_TIMER = 60

	def BuildServer(self,port_no,num_clients):
		"""Builds The server on the port_number port_no for num_clients
		Args:
			port_no: (int) The port number
			num_clients: (int) The number of clients who would join (>= 2 for all practical purposes)
		Returns: 
			None		
		"""
		s = socket.socket()
		host = socket.gethostname()
		self.port = port_no		
		s.bind((host,port_no))
		s.listen(5)
		client_count = 0
		# TODO : Handle TIMEOUT using signal
		while client_count < num_clients:			
			c,addr = s.accept()
			client_count += 1
			self.communicator_list.append(Communicator())
			self.communicator_list[-1].setSocket(c)
		s.close()

	
	def setNetworkTimer(self,Time_in_seconds):
		self.NETWORK_TIMER = Time_in_seconds
	
	def getNetworkTimer(self):
		return self.NETWORK_TIMER

	def RecvDataFromClient(self,client_id):		
		"""Receives Data from Client client_id
		Args: 
			client_id: The integer index of a client
		Returns: 
			data: Received on the socket to client_id, None in case of an Error
		"""
		data = None
		if(client_id < len(self.communicator_list)):					
			data = self.communicator_list[client_id].RecvDataOnSocket(self.NETWORK_TIMER)
			if(data is None):
				print 'ERROR : TIMEOUT ON CLIENT NETWORK' + str(client_id) + ' END'
				self.CloseClient(client_id)
		return data

	def SendData2Client(self,client_id,data):		
		"""Sends data to the Client client_id. In case data was None, sends the 
		   appropriate data (with ACTION='KILLPROC') and closes the socket
		Args:
			client_id : (int) client_id
			data : The json file to be sent, or None in case of an Error
		Returns:
			success_flag : True if send was successful
		"""
		success_flag = False
		if(data is None):
			data = {'meta': 'TIMEOUT ON CLIENT NETWORK', 'action':'KILLPROC','data':''}
		else:
			data = json.loads(data)

		if(client_id < len(self.communicator_list)):			
			success_flag = self.communicator_list[client_id].SendDataOnSocket(json.dumps(data))			
			if(not success_flag):
				print 'ERROR : COULD NOT SEND DATA TO CLIENT ' + str(client_id)
				self.CloseClient(client_id)
			elif((data['action'] == 'KILLPROC') or (data['action'] == 'FINISH')):
				self.CloseClient(client_id)			
		return success_flag

	def CloseClient(self,client_id):
		"""Closes the client with client_id client_id
		Args:
			client_id : (int) index of client
		Returns:
			None
		"""		
		if(client_id < len(self.communicator_list)):
			self.communicator_list[client_id] = None
	
	def CloseAllClients(self):
		"""Closes all clients in the communicator_list and resets the communicator_list
		Args:
			None
		Returns:
			None
		"""
		for idx in xrange(len(self.communicator_list)):
			if(not self.communicator_list[idx] is None):
				self.CloseClient(idx)
		self.communicator_list = []

if __name__ == '__main__':
	print 'Start'
	local_Server = Server()
	local_Server.BuildServer(int(sys.argv[1]), 2)
	data = {'meta':'', 'action':'INIT','data':'1 5 120'}
	local_Server.SendData2Client(0, json.dumps(data))
	data['data'] = '2 5 120'
	local_Server.SendData2Client(1, json.dumps(data))
	
	while(True):
		data = local_Server.RecvDataFromClient(0)
		local_Server.SendData2Client(1, data)
		if not data:
			break
		print data, 'Received from client 0'
		data = json.loads(data)
		if data['action'] == 'FINISH' or data['action'] == 'KILLPROC':
			break		
		data = local_Server.RecvDataFromClient(1)
		print data, 'Received from client 1'
		local_Server.SendData2Client(0, data)
		if not data:
			break
		data = json.loads(data)
		if data['action'] == 'FINISH' or data['action'] == 'KILLPROC':
			break
