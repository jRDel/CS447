
import socket
import sys
import subprocess
from datetime import datetime, date, time, timedelta

TCP_IP = 'cs447-newellz2-server.ncr'
TCP_PORT = 37
BUFFER_SIZE = 1024
MESSAGE = b''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
data = int.from_bytes(data, byteorder=sys.byteorder)

tsecs = timedelta(seconds=data)
timepro = datetime(year=1900, month=1, day=1, hour=0, minute=0, second=0)
timefrom = timepro+tsecs

if data<2208988800:
	print(timefrom)
	sys.exit("Will not set the date because seconds are before January 1st, 1970 (Linux Epoch)");	

s.close()

string=str(timefrom) #get the string format of the datetime object added with timedelta
cmd = ['date', '-s', string] #subprocess command to set time to the string
subprocess.call(cmd)

