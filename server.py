import sys
from cache import Cache, Record
from socket import socket, AF_INET, SOCK_DGRAM

# Get command line arguments.
is_resolver = sys.argv[1]
file_path = sys.argv[2]

# Load initial data into the cache from the mappings file.
server_cache = Cache()
server_cache.load_file(file_path)

s = socket(AF_INET, SOCK_DGRAM)
source_ip = '127.0.0.1'
source_port = 12345
s.bind((source_ip, source_port))
while True:
    data, sender_info = s.recvfrom(2048)
    print "Message: ", data, " from: ", sender_info
    s.sendto(data.upper(), sender_info)
