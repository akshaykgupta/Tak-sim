from Communicator import Communicator
import socket,sys
class Client(Communicator):
	def __init__(self):
		pass

	def Connect2Server(self,server_address,port_no):
		self.clientSocket = socket.socket()
		self.clientSocket.connect((server_address,port_no))
		self.setSocket(self.clientSocket)

	def SendData2Server(self,data):		
		self.SendDataOnSocket(data)

	def RecvDataFromServer(self):
		# --- TODO: HANDLE DIFFERENT DATA RECEIVED --- #
		data = self.RecvDataOnSocket()
		return data


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
		client.SendDataOnPipe(str(counter) + '\n')
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



	

