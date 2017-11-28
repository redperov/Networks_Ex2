import sys
from parser_commands import parse_ip_port
from dns import DnsRequest
from socket import socket, AF_INET, SOCK_DGRAM

# Get command line arguments.
# The format: [resolver_ip:resolver:port]
dest_ip, dest_port = parse_ip_port(sys.argv[1])

# Create a UDP socket.
s = socket(AF_INET, SOCK_DGRAM)

msg = raw_input("Message to send: ")
while not msg == 'quit':
    # Create a dns request.
    s.sendto(msg, (dest_ip, dest_port))
    response, _ = s.recvfrom(2048)
    print "Server sent: ", response
    msg = raw_input("Message to send: ")
s.close()
