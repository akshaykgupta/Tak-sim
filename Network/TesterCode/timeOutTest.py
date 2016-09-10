import sys
sys.path.append('/Users/barunpatra/Desktop/Barun/IIT/Semester\ V/TA_AI/Tak-sim/Network/')
import client as clnt
client = clnt.Client()
# client.CreateChildProcess('python','Exception.py')
client.CreateChildProcess('python','run.sh')
data = client.RecvDataFromProcess()
client.SendData2Process(data)
print data

