import client,time,sys
client = client.Client()
client.Connect2Server(sys.argv[1],int(sys.argv[2]))
num_from_server = client.RecvDataOnSocket(20)
print num_from_server
time.sleep(60)
client.SendDataOnSocket(str(int(num_from_server) + 1))