import sys
from server import Server
from socket import socket, AF_INET, SOCK_DGRAM

# Get command line arguments.
is_resolver = sys.argv[1]
file_path = sys.argv[2]

# Create a server with a cache.
server = Server(is_resolver, file_path)

# Create a UDP socket.
s = socket(AF_INET, SOCK_DGRAM)

source_ip = '127.0.0.1'
source_port = 12345
s.bind((source_ip, source_port))
while True:
    request, sender_info = s.recvfrom(2048)
    print "Message: ", request, " from: ", sender_info
    answer = str(server.handle_request(request))
    s.sendto(answer, sender_info)
