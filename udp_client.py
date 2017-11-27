import sys
from socket import socket, AF_INET, SOCK_DGRAM

# Get command line arguments.
dest_port = int(sys.argv[1])

# Create a UDP socket.
s = socket(AF_INET, SOCK_DGRAM)
dest_ip = '127.0.0.1'
msg = raw_input("Message to send: ")
while not msg == 'quit':
    s.sendto(msg, (dest_ip, dest_port))
    data, _ = s.recvfrom(2048)
    print "Server sent: ", data
    msg = raw_input("Message to send: ")
s.close()
