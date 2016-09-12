import socket,sys,json
from Communicator import Communicator

class Server:
	def __init__(self):
		self.communicator_list = []

	def BuildServer(self,port_no,num_clients):
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
	
	def RecvDataFromClient(self,client_id,TIMEOUT=20):		
		data = None
		if(client_id < len(self.communicator_list)):					
			data = self.communicator_list[client_id].RecvDataOnSocket(TIMEOUT)
			if(data is None):
				print 'ERROR : TIMEOUT ON CLIENT ' + str(client_id) + ' END'
				self.communicator_list[client_id].closeSocket()
		return data

	def SendData2Client(self,client_id,data):		
		success_flag = False
		if(client_id < len(self.communicator_list)):			
			success_flag = self.communicator_list[client_id].SendDataOnSocket(data)
			if(not success_flag):
				print 'ERROR : COULD NOT SEND DATA TO CLIENT ' + str(client_id)
				self.communicator_list[client_id].closeSocket()
				self.communicator_list[client_id] = None
		return success_flag

	def CloseClient(self,client_id):		
		if(client_id < len(self.communicator_list)):
			self.communicator_list[client_id].closeSocket()
			self.communicator_list[client_id] = None
	
	def CloseAllClients(self):
		for idx in xrange(len(self.communicator_list)):
			if(not self.communicator_list[idx] is None):
				self.communicator_list[idx].closeSocket()
				self.communicator_list[idx] = None
		self.communicator_list = []



if __name__ == '__main__':
	print 'Start'
	local_Server = Server()
	local_Server.BuildServer(int(sys.argv[1]),2)
	while 1:
		num_from_0 = local_Server.RecvDataFromClient(0)
		local_Server.SendData2Client(1,num_from_0)
		num_from_1 = local_Server.RecvDataFromClient(1)
		local_Server.SendData2Client(0,num_from_1)
		if(int(num_from_1) == 100):
			local_Server.SendData2Client(1,str(int(num_from_1) + 1))
			break
	local_Server.CloseClient(0)
	local_Server.CloseClient(1)



