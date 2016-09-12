import Communicator,server,sys

local_Server = server.Server()
local_Server.BuildServer(int(sys.argv[1]),1)
num_from_0 = str(1)
local_Server.SendData2Client(0,num_from_0)
num_from_0 = local_Server.RecvDataFromClient(0)

