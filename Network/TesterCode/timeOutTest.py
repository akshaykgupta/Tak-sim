import sys,time
import client as clnt
client = clnt.Client()
client.CreateChildProcess('python','exitsFast.py')
time.sleep(10)
data = 'This should not reach \n'
client.SendData2Process(data)


