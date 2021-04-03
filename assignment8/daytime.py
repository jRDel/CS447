import socket
import subprocess

TCP_IP = 'cs447-newellz2-server.ncr'
TCP_PORT = 13
BUFFER_SIZE = 1024
MESSAGE = b''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)

string=str(data.decode('utf-8'))

cmd = ['date', '-s', string]
subprocess.call(cmd)

s.close()

#print ("received data:",  data.decode('utf-8'))
